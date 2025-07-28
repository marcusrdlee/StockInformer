#!/usr/bin/env python3
"""
Debug script to see what's happening in portfolio planning
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
from investment_agent.agent import step_2_build_portfolio, PortfolioPlan, PortfolioAllocation

async def debug_portfolio():
    """Debug the portfolio planning step."""
    
    print("🔍 Debugging Portfolio Planning")
    print("=" * 50)
    
    # Create a test state with research results
    state = InvestmentAgentState(
        risk_level="Medium",
        industry="Big tech",
        investment_amount=100000.0,
        time_horizon="1 year",
        research_results=[
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
    )
    
    print(f"Research results: {state.research_results}")
    
    try:
        # Try to build portfolio
        result = await step_2_build_portfolio(state, {})
        
        print(f"✅ Portfolio planning completed!")
        print(f"Portfolio plan: {result.portfolio_plan}")
        
        if result.portfolio_plan:
            print(f"Number of companies: {len(result.portfolio_plan['companies'])}")
            print(f"Total allocation: {result.portfolio_plan['total_allocation']}%")
            
            for company in result.portfolio_plan['companies']:
                print(f"  {company['company_name']}: {company['allocation_percentage']}%")
        else:
            print("❌ No portfolio plan generated")
            
    except Exception as e:
        print(f"❌ Error in portfolio planning: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_portfolio()) 