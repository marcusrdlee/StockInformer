#!/usr/bin/env python3
"""
Debug script to see what the result object contains
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv("secrets.env")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Import the investment agent
from code.investment_agent import InvestmentAgentState, graph

async def debug_result():
    """Debug the result object."""
    
    # Investment Profile
    risk_level = "Medium"
    industry = "Big tech"
    investment_amount = 100000.0
    time_horizon = "1 year"
    
    # Create investment plan
    state = InvestmentAgentState(
        risk_level=risk_level,
        industry=industry,
        investment_amount=investment_amount,
        time_horizon=time_horizon
    )
    
    try:
        # Execute the investment planning workflow
        result = await graph.ainvoke(state)
        print("✅ Investment plan generated successfully!")
        
        # Debug the result object
        print("\n" + "=" * 50)
        print("🔍 DEBUG RESULT OBJECT")
        print("=" * 50)
        
        print(f"Result type: {type(result)}")
        print(f"Result attributes: {dir(result)}")
        
        if hasattr(result, '__dict__'):
            print(f"Result dict: {result.__dict__}")
        
        # Try to access the state directly
        if hasattr(result, 'risk_level'):
            print(f"Risk level: {result.risk_level}")
        if hasattr(result, 'research_results'):
            print(f"Research results: {result.research_results}")
        if hasattr(result, 'portfolio_plan'):
            print(f"Portfolio plan: {result.portfolio_plan}")
        if hasattr(result, 'investment_plan'):
            print(f"Investment plan: {result.investment_plan}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_result()) 