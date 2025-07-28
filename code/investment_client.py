#!/usr/bin/env python3
"""
Investment Planning Agent Client

This script demonstrates the personalized investment planning agent that creates 
customized investment portfolios based on user preferences.
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../variables.env")
load_dotenv("../secrets.env")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the investment agent
from investment_agent import InvestmentAgentState, graph


async def main():
    """Main function to demonstrate the investment planning agent."""
    
    print("🤖 Investment Planning Agent")
    print("=" * 50)
    
    # Investment Profile
    risk_level = "Medium"  # Low, Medium, or High
    industry = "Big tech"  # Optional: specific industry focus
    investment_amount = 100000.0  # Amount to invest in dollars
    time_horizon = "1 year"  # Investment time horizon
    
    print(f"Creating investment plan for:")
    print(f"Risk Level: {risk_level}")
    print(f"Industry: {industry}")
    print(f"Investment Amount: ${investment_amount:,.2f}")
    print(f"Time Horizon: {time_horizon}")
    print("\nProcessing... This may take a few minutes.")
    print("-" * 50)
    
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
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 PORTFOLIO SUMMARY")
        print("=" * 50)
        
        if result.portfolio_plan:
            print("Portfolio Allocation:")
            print("-" * 50)
            for company in result.portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * investment_amount
                print(f"{company['company_name']:<25} {allocation:>6.1f}% ${amount:>10,.2f}")
            print("-" * 50)
            print(f"Total Allocation: {result.portfolio_plan['total_allocation']:.1f}%")
        
        print("\n" + "=" * 50)
        print("🔍 RESEARCH RESULTS")
        print("=" * 50)
        
        if result.research_results:
            for i, company in enumerate(result.research_results, 1):
                print(f"{i}. {company['name']}")
                print(f"   Risk: {company['risk_factor']}")
                print(f"   Reason: {company['explanation']}")
                print()
        
        print("\n" + "=" * 50)
        print("📋 FINAL INVESTMENT PLAN")
        print("=" * 50)
        
        if result.investment_plan:
            print(result.investment_plan)
        else:
            print("No investment plan generated.")
            
    except Exception as e:
        logger.error(f"Error generating investment plan: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 