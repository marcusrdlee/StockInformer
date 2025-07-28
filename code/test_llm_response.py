#!/usr/bin/env python3
"""
Test to see what the LLM is returning for portfolio planning
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv("secrets.env")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Import the investment agent
from investment_agent import InvestmentAgentState
from investment_agent.agent import llm, PortfolioPlan
from investment_agent.prompts import portfolio_planning_prompt

async def test_llm_response():
    """Test what the LLM returns for portfolio planning."""
    
    print("🔍 Testing LLM Response for Portfolio Planning")
    print("=" * 50)
    
    # Create test data
    companies = [
        {
            "name": "Apple Inc.",
            "risk_factor": "Medium",
            "explanation": "Strong tech company"
        },
        {
            "name": "Microsoft Corp.",
            "risk_factor": "Medium", 
            "explanation": "Cloud leader"
        },
        {
            "name": "NVIDIA Corp.",
            "risk_factor": "Medium",
            "explanation": "AI leader"
        }
    ]
    
    # Create the prompt
    system_prompt = portfolio_planning_prompt.format(
        companies=companies,
        risk_level="Medium",
        investment_amount=100000.0,
        time_horizon="1 year",
    )
    
    print("System prompt:")
    print("-" * 30)
    print(system_prompt)
    print("-" * 30)
    
    try:
        # Test with structured output
        model = llm.with_structured_output(PortfolioPlan)
        messages = [{"role": "system", "content": system_prompt}]
        
        print("\nCalling LLM with structured output...")
        response = await model.ainvoke(messages)
        
        print(f"✅ LLM Response: {response}")
        
        if response:
            print(f"Number of companies: {len(response.companies)}")
            print(f"Total allocation: {response.total_allocation}%")
            
            for company in response.companies:
                print(f"  {company.company_name}: {company.allocation_percentage}%")
        else:
            print("❌ No response from LLM")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_llm_response()) 