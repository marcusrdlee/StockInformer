#!/usr/bin/env python3
"""
Example Usage of the Investment Planning Agent

This script demonstrates different investment scenarios using the agent.
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
from investment_agent import create_investment_plan


def example_1_conservative_investor():
    """Example 1: Conservative investor with low risk tolerance."""
    print("📈 Example 1: Conservative Investor")
    print("=" * 50)
    
    plan = create_investment_plan(
        risk_level="Low",
        industry="Healthcare",
        investment_amount=50000.0,
        time_horizon="3 years"
    )
    
    if plan and plan.investment_plan:
        print("✅ Investment plan created successfully!")
        print("\nPortfolio Summary:")
        if plan.portfolio_plan:
            for company in plan.portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * 50000
                print(f"  {company['company_name']}: {allocation:.1f}% (${amount:,.2f})")
    else:
        print("❌ Failed to create investment plan")


def example_2_aggressive_investor():
    """Example 2: Aggressive investor with high risk tolerance."""
    print("\n📈 Example 2: Aggressive Investor")
    print("=" * 50)
    
    plan = create_investment_plan(
        risk_level="High",
        industry="Technology",
        investment_amount=200000.0,
        time_horizon="5 years"
    )
    
    if plan and plan.investment_plan:
        print("✅ Investment plan created successfully!")
        print("\nPortfolio Summary:")
        if plan.portfolio_plan:
            for company in plan.portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * 200000
                print(f"  {company['company_name']}: {allocation:.1f}% (${amount:,.2f})")
    else:
        print("❌ Failed to create investment plan")


def example_3_balanced_investor():
    """Example 3: Balanced investor with medium risk tolerance."""
    print("\n📈 Example 3: Balanced Investor")
    print("=" * 50)
    
    plan = create_investment_plan(
        risk_level="Medium",
        industry=None,  # No specific industry focus
        investment_amount=100000.0,
        time_horizon="2 years"
    )
    
    if plan and plan.investment_plan:
        print("✅ Investment plan created successfully!")
        print("\nPortfolio Summary:")
        if plan.portfolio_plan:
            for company in plan.portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * 100000
                print(f"  {company['company_name']}: {allocation:.1f}% (${amount:,.2f})")
    else:
        print("❌ Failed to create investment plan")


def main():
    """Run all examples."""
    print("🤖 Investment Planning Agent - Examples")
    print("=" * 60)
    
    try:
        example_1_conservative_investor()
        example_2_aggressive_investor()
        example_3_balanced_investor()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed!")
        print("\nTo run the full agent with real-time data:")
        print("1. Set up your SERPAPI_API_KEY in secrets.env")
        print("2. Run: python code/investment_client.py")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 