#!/usr/bin/env python3
"""
Test with actual research results from Step 1
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

async def test_real_data():
    """Test with actual research results from Step 1."""
    
    print("🔍 Testing with Real Research Data")
    print("=" * 50)
    
    # Use the actual research results from Step 1
    companies = [
        {'name': 'Apple Inc.', 'risk_factor': 'Medium', 'explanation': 'Apple has a strong market position, competitive advantages, and consistent financial performance. Its growth potential is aligned with the 1-year time horizon, and its risk profile is suitable for a medium-risk investor.'},
        {'name': 'Microsoft Corp.', 'risk_factor': 'Medium', 'explanation': 'Microsoft has a strong market position, competitive advantages, and consistent financial performance. Its growth potential is aligned with the 1-year time horizon, and its risk profile is suitable for a medium-risk investor.'},
        {'name': 'Nvidia Corp.', 'risk_factor': 'Medium', 'explanation': 'Nvidia has a strong market position, competitive advantages, and consistent financial performance. Its growth potential is aligned with the 1-year time horizon, and its risk profile is suitable for a medium-risk investor.'}
    ]
    
    print(f"Number of companies: {len(companies)}")
    print(f"First company: {companies[0]}")
    
    # Create the prompt
    system_prompt = portfolio_planning_prompt.format(
        companies=companies,
        risk_level="Medium",
        investment_amount=100000.0,
        time_horizon="1 year",
    )
    
    print(f"\nPrompt length: {len(system_prompt)} characters")
    
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
    asyncio.run(test_real_data()) 