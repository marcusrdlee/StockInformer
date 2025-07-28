"""
The main agent that orchestrates the investment planning process.
"""

import logging
import os
from typing import Annotated, Any, Sequence, cast

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import tools
from .prompts import (
    company_research_prompt,
    portfolio_planning_prompt,
    investment_rationale_prompt,
    final_report_prompt,
)

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)


class CompanyResearch(BaseModel):
    name: str
    risk_factor: str
    explanation: str


class CompanyResearchList(BaseModel):
    companies: list[CompanyResearch]


class PortfolioAllocation(BaseModel):
    company_name: str
    allocation_percentage: float
    holding_period: str | None = None


class PortfolioPlan(BaseModel):
    companies: list[PortfolioAllocation]
    total_allocation: float


class InvestmentAgentState(BaseModel):
    risk_level: str
    industry: str | None
    investment_amount: float
    time_horizon: str
    research_results: list[dict] | None = None
    portfolio_plan: dict | None = None
    investment_rationale: str | None = None
    investment_plan: str | None = None
    messages: Annotated[Sequence[Any], add_messages] = []


async def step_1_research_companies(state: InvestmentAgentState, config: RunnableConfig):
    """Step 1: Research companies in the selected industry."""
    _LOGGER.info("Step 1: Researching companies for investment planning.")

    # Use SerpAPI to search for companies
    search_query = f"top companies {state.industry or 'technology'} industry investment potential {state.time_horizon}"
    
    search_results = await tools.search_companies(search_query)
    
    # Process results with LLM to extract structured company data
    model = llm.with_structured_output(CompanyResearchList)
    
    system_prompt = company_research_prompt.format(
        industry=state.industry or "technology",
        risk_level=state.risk_level,
        time_horizon=state.time_horizon,
        search_results=search_results,
    )
    
    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}]
        response = await model.ainvoke(messages, config)
        if response:
            company_list = cast(CompanyResearchList, response)
            research_results = [
                {
                    "name": company.name,
                    "risk_factor": company.risk_factor,
                    "explanation": company.explanation,
                }
                for company in company_list.companies
            ]
            state.research_results = research_results
            return state
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )
    
    raise RuntimeError("Failed to process company research after %d attempts.", _MAX_LLM_RETRIES)


async def step_2_build_portfolio(state: InvestmentAgentState, config: RunnableConfig):
    """Step 2: Build portfolio plan based on research results."""
    _LOGGER.info("Step 2: Building portfolio plan.")
    
    if not state.research_results:
        raise ValueError("Research results are required for portfolio planning.")
    
    model = llm.with_structured_output(PortfolioPlan)
    
    system_prompt = portfolio_planning_prompt.format(
        companies=state.research_results,
        risk_level=state.risk_level,
        investment_amount=state.investment_amount,
        time_horizon=state.time_horizon,
    )
    
    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            response = await model.ainvoke(messages, config)
            _LOGGER.info(f"Step 2 LLM response (attempt {count + 1}): {response}")
            
            if response and hasattr(response, 'companies') and len(response.companies) > 0:
                portfolio = cast(PortfolioPlan, response)
                state.portfolio_plan = {
                    "companies": [
                        {
                            "company_name": company.company_name,
                            "allocation_percentage": company.allocation_percentage,
                            "holding_period": company.holding_period,
                        }
                        for company in portfolio.companies
                    ],
                    "total_allocation": portfolio.total_allocation,
                }
                _LOGGER.info(f"Step 2 portfolio plan created: {state.portfolio_plan}")
                return state
            elif response and hasattr(response, 'companies') and len(response.companies) == 0:
                # LLM returned empty portfolio, create a fallback
                _LOGGER.warning("LLM returned empty portfolio, creating fallback allocation")
                from investment_agent.agent import PortfolioAllocation
                
                # Create a simple equal allocation for the first 5 companies
                companies_to_allocate = state.research_results[:5]
                allocation_per_company = 100.0 / len(companies_to_allocate)
                
                fallback_companies = [
                    {
                        "company_name": company["name"],
                        "allocation_percentage": allocation_per_company,
                        "holding_period": "6-12 months",
                    }
                    for company in companies_to_allocate
                ]
                
                state.portfolio_plan = {
                    "companies": fallback_companies,
                    "total_allocation": 100.0,
                }
                _LOGGER.info(f"Step 2 fallback portfolio plan created: {state.portfolio_plan}")
                return state
                
        except Exception as e:
            _LOGGER.warning(f"LLM call failed (attempt {count + 1}): {e}")
            if count == _MAX_LLM_RETRIES - 1:
                # Last attempt failed, create fallback
                _LOGGER.warning("All LLM attempts failed, creating fallback allocation")
                from investment_agent.agent import PortfolioAllocation
                
                # Create a simple equal allocation for the first 5 companies
                companies_to_allocate = state.research_results[:5]
                allocation_per_company = 100.0 / len(companies_to_allocate)
                
                fallback_companies = [
                    {
                        "company_name": company["name"],
                        "allocation_percentage": allocation_per_company,
                        "holding_period": "6-12 months",
                    }
                    for company in companies_to_allocate
                ]
                
                state.portfolio_plan = {
                    "companies": fallback_companies,
                    "total_allocation": 100.0,
                }
                _LOGGER.info(f"Step 2 emergency fallback portfolio plan created: {state.portfolio_plan}")
                return state
    
    raise RuntimeError("Failed to build portfolio plan after %d attempts.", _MAX_LLM_RETRIES)


async def step_3_generate_rationale(state: InvestmentAgentState, config: RunnableConfig):
    """Step 3: Generate investment rationale for each selected company."""
    _LOGGER.info("Step 3: Generating investment rationale.")
    
    if not state.portfolio_plan or not state.research_results:
        raise ValueError("Portfolio plan and research results are required.")
    
    system_prompt = investment_rationale_prompt.format(
        portfolio_plan=state.portfolio_plan,
        research_results=state.research_results,
        risk_level=state.risk_level,
        industry=state.industry or "technology",
        time_horizon=state.time_horizon,
    )
    
    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}]
        response = await llm.ainvoke(messages, config)
        if response and response.content:
            state.investment_rationale = response.content
            return state
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )
    
    raise RuntimeError("Failed to generate investment rationale after %d attempts.", _MAX_LLM_RETRIES)


async def step_4_format_final_report(state: InvestmentAgentState, config: RunnableConfig):
    """Step 4: Format the final investment plan report."""
    _LOGGER.info("Step 4: Formatting final investment plan report.")
    
    if not state.portfolio_plan or not state.investment_rationale:
        raise ValueError("Portfolio plan and investment rationale are required.")
    
    system_prompt = final_report_prompt.format(
        portfolio_plan=state.portfolio_plan,
        investment_rationale=state.investment_rationale,
        risk_level=state.risk_level,
        industry=state.industry or "technology",
        investment_amount=state.investment_amount,
        time_horizon=state.time_horizon,
    )
    
    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}]
        response = await llm.ainvoke(messages, config)
        if response and response.content:
            state.investment_plan = response.content
            return state
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )
    
    raise RuntimeError("Failed to format final report after %d attempts.", _MAX_LLM_RETRIES)


# Build the workflow graph
workflow = StateGraph(InvestmentAgentState)

workflow.add_node("step_1_research_companies", step_1_research_companies)
workflow.add_node("step_2_build_portfolio", step_2_build_portfolio)
workflow.add_node("step_3_generate_rationale", step_3_generate_rationale)
workflow.add_node("step_4_format_final_report", step_4_format_final_report)

workflow.add_edge(START, "step_1_research_companies")
workflow.add_edge("step_1_research_companies", "step_2_build_portfolio")
workflow.add_edge("step_2_build_portfolio", "step_3_generate_rationale")
workflow.add_edge("step_3_generate_rationale", "step_4_format_final_report")
workflow.add_edge("step_4_format_final_report", END)

graph = workflow.compile() 