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


def _get_llm():
    """Get the LLM instance, creating it if needed."""
    import os

    api_key = os.getenv("NVIDIA_API_KEY")
    return ChatNVIDIA(
        model="meta/llama-3.3-70b-instruct", temperature=0, api_key=api_key
    )


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


async def step_1_research_companies(
    state: InvestmentAgentState, config: RunnableConfig
):
    """Step 1: Research companies in the selected industry."""
    _LOGGER.info("Step 1: Researching companies for investment planning.")

    # Use SerpAPI to search for companies
    industry = state.industry or "technology"
    search_query = f"best {industry} stocks to invest 2025 top companies"

    search_results = await tools.search_companies(search_query)

    # Process results with LLM to extract structured company data
    model = _get_llm().with_structured_output(CompanyResearchList)

    system_prompt = company_research_prompt.format(
        industry=state.industry or "technology",
        risk_level=state.risk_level,
        time_horizon=state.time_horizon,
        search_results=search_results,
    )

    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            response = await model.ainvoke(messages, config)

            # Process the response
            if (
                response
                and hasattr(response, "companies")
                and len(response.companies) > 0
            ):
                state.research_results = [
                    {
                        "name": company.name,
                        "risk_factor": company.risk_factor,
                        "explanation": company.explanation,
                    }
                    for company in response.companies
                ]
                _LOGGER.info(
                    f"Step 1 research completed: {len(state.research_results)} companies found"
                )
                return state
            else:
                _LOGGER.warning(f"LLM returned no companies (attempt {count + 1})")

        except Exception as e:
            _LOGGER.warning(f"LLM call failed (attempt {count + 1}): {e}")
            if count == _MAX_LLM_RETRIES - 1:
                # This was the last attempt
                _LOGGER.error(
                    "All LLM attempts failed in step_1_research_companies. No fallback data will be provided."
                )

    raise RuntimeError(
        "Failed to process company research after %d attempts.", _MAX_LLM_RETRIES
    )


async def step_2_build_portfolio(state: InvestmentAgentState, config: RunnableConfig):
    """Step 2: Build investment portfolio plan."""
    _LOGGER.info("Step 2: Building portfolio plan.")

    if not state.research_results:
        raise RuntimeError("No research results available for portfolio planning")

    # Create structured output model for portfolio planning
    model = _get_llm().with_structured_output(PortfolioPlan)

    # Build system prompt with research results
    company_details = "\n".join(
        [
            f"- {company['name']}: {company['explanation']} (Risk: {company['risk_factor']})"
            for company in state.research_results
        ]
    )

    system_prompt = portfolio_planning_prompt.format(
        companies=company_details,
        risk_level=state.risk_level,
        investment_amount=state.investment_amount,
        time_horizon=state.time_horizon,
    )

    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            response = await model.ainvoke(messages, config)

            if (
                response
                and hasattr(response, "companies")
                and len(response.companies) > 0
            ):
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
            elif (
                response
                and hasattr(response, "companies")
                and len(response.companies) == 0
            ):
                # LLM returned empty portfolio, create a fallback
                _LOGGER.warning(
                    "LLM returned empty portfolio, creating fallback allocation"
                )
                from investment_agent.agent import PortfolioAllocation

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
                _LOGGER.info(
                    f"Step 2 fallback portfolio plan created: {state.portfolio_plan}"
                )
                return state

        except Exception as e:
            _LOGGER.warning(f"LLM call failed (attempt {count + 1}): {e}")
            if count == _MAX_LLM_RETRIES - 1:
                # Last attempt failed, create fallback portfolio
                _LOGGER.warning("All LLM attempts failed, creating fallback allocation")

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
                _LOGGER.info(
                    f"Step 2 emergency fallback portfolio plan created: {state.portfolio_plan}"
                )
                return state

    raise RuntimeError(
        "Failed to build portfolio plan after %d attempts.", _MAX_LLM_RETRIES
    )


async def step_3_generate_rationale(
    state: InvestmentAgentState, config: RunnableConfig
):
    """Step 3: Generate investment rationale for each selected company."""
    _LOGGER.info("Step 3: Generating investment rationale.")

    if not state.portfolio_plan:
        raise RuntimeError("No portfolio plan available for rationale generation")

    # Build system prompt with portfolio and research data
    portfolio_details = "\n".join(
        [
            f"- {company['company_name']}: {company['allocation_percentage']}% allocation"
            for company in state.portfolio_plan["companies"]
        ]
    )

    research_details = "\n".join(
        [
            f"- {company['name']}: {company['explanation']} (Risk: {company['risk_factor']})"
            for company in state.research_results or []
        ]
    )

    system_prompt = investment_rationale_prompt.format(
        portfolio_plan=portfolio_details,
        research_results=research_details,
        risk_level=state.risk_level,
        industry=state.industry or "technology",
        time_horizon=state.time_horizon,
    )

    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            response = await _get_llm().ainvoke(messages, config)

            if response and response.content:
                state.investment_rationale = response.content
                _LOGGER.info("Step 3 investment rationale generated successfully")
                return state

        except Exception as e:
            _LOGGER.warning(f"LLM call failed (attempt {count + 1}): {e}")
            if count == _MAX_LLM_RETRIES - 1:
                # Last attempt failed, create fallback rationale
                _LOGGER.warning(
                    "All Step 3 LLM attempts failed, creating fallback rationale"
                )

                fallback_rationale = f"""
## Investment Rationale

Based on our analysis, we have selected the following companies for your {state.risk_level.lower()}-risk investment portfolio of ${state.investment_amount:,.2f} over a {state.time_horizon} timeframe:

"""

                for company in state.portfolio_plan["companies"]:
                    company_name = company["company_name"]
                    allocation = company["allocation_percentage"]

                    # Find the research data for this company
                    research_data = next(
                        (
                            c
                            for c in state.research_results
                            if c["name"] == company_name
                        ),
                        None,
                    )

                    if research_data:
                        fallback_rationale += f"""
### {company_name} ({allocation}% allocation)
{research_data['explanation']}

"""

                state.investment_rationale = fallback_rationale.strip()
                _LOGGER.info("Step 3 fallback rationale created")
                return state

    raise RuntimeError(
        "Failed to generate investment rationale after %d attempts.", _MAX_LLM_RETRIES
    )


async def step_4_format_final_report(
    state: InvestmentAgentState, config: RunnableConfig
):
    """Step 4: Format the final investment plan report."""
    _LOGGER.info("Step 4: Formatting final investment plan report.")

    if not state.portfolio_plan or not state.investment_rationale:
        raise RuntimeError(
            "Missing portfolio plan or investment rationale for final report"
        )

    # Build system prompt with all accumulated data
    portfolio_summary = (
        f"Total allocation: {state.portfolio_plan['total_allocation']}%\n"
    )
    portfolio_summary += "\n".join(
        [
            f"- {company['company_name']}: {company['allocation_percentage']}% "
            f"(${(company['allocation_percentage'] / 100) * state.investment_amount:,.2f})"
            for company in state.portfolio_plan["companies"]
        ]
    )

    system_prompt = final_report_prompt.format(
        risk_level=state.risk_level,
        industry=state.industry or "technology",
        investment_amount=state.investment_amount,
        time_horizon=state.time_horizon,
        portfolio_plan=portfolio_summary,
        investment_rationale=state.investment_rationale,
    )

    for count in range(_MAX_LLM_RETRIES):
        try:
            messages = [{"role": "system", "content": system_prompt}]
            response = await _get_llm().ainvoke(messages, config)

            if response and response.content:
                state.investment_plan = response.content
                _LOGGER.info("Step 4 final investment plan report generated")
                return state

        except Exception as e:
            _LOGGER.warning(f"LLM call failed (attempt {count + 1}): {e}")
            if count == _MAX_LLM_RETRIES - 1:
                # Last attempt failed, create fallback report
                _LOGGER.warning(
                    "All Step 4 LLM attempts failed, creating fallback report"
                )

                fallback_report = f"""
# Personalized Investment Plan

## Executive Summary
This investment plan has been created for a {state.risk_level.lower()}-risk investor with ${state.investment_amount:,.2f} to invest over a {state.time_horizon} timeframe.

## Portfolio Allocation

| Company | Allocation | Amount | Holding Period | Risk Level |
|---------|------------|--------|----------------|------------|
"""

                for company in state.portfolio_plan["companies"]:
                    company_name = company["company_name"]
                    allocation = company["allocation_percentage"]
                    amount = (allocation / 100) * state.investment_amount
                    holding_period = company.get("holding_period", "6-12 months")

                    # Find the research data for this company
                    research_data = next(
                        (
                            c
                            for c in state.research_results
                            if c["name"] == company_name
                        ),
                        None,
                    )
                    risk_level = (
                        research_data["risk_factor"] if research_data else "Medium"
                    )

                    fallback_report += f"| {company_name} | {allocation}% | ${amount:,.2f} | {holding_period} | {risk_level} |\n"

                fallback_report += f"""

## Investment Rationale
{state.investment_rationale}

## Risk Considerations
This portfolio is designed for {state.risk_level.lower()}-risk tolerance and should be reviewed regularly.
"""

                state.investment_plan = fallback_report.strip()
                _LOGGER.info("Step 4 fallback report created")
                return state

    raise RuntimeError(
        "Failed to format final report after %d attempts.", _MAX_LLM_RETRIES
    )


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
