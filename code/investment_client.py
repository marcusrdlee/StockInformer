#!/usr/bin/env python3
"""
Investment Planning Agent Client

This script demonstrates the personalized investment planning agent that creates
customized investment portfolios based on user preferences.
"""
# Import the investment agent and terminal helper

from investment_agent import InvestmentAgentState, graph
from terminal_helper import get_user_investment_profile


import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv("variables.env")
load_dotenv("secrets.env")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main function to demonstrate the investment planning agent."""

    # Get user input interactively
    profile = get_user_investment_profile()

    print("\nProcessing... This may take a few minutes.")
    print("-" * 50)

    # Create investment plan
    state = InvestmentAgentState(
        risk_level=profile["risk_level"],
        industry=profile["industry"],
        investment_amount=profile["investment_amount"],
        time_horizon=profile["time_horizon"],
    )

    try:
        # Execute the investment planning workflow
        result = await graph.ainvoke(state)
        print("✅ Investment plan generated successfully!")

        # Display results
        print("\n" + "=" * 50)
        print("📊 PORTFOLIO SUMMARY")
        print("=" * 50)

        # Handle both Pydantic models and dictionaries
        if isinstance(result, dict):
            portfolio_plan = result.get("portfolio_plan")
            research_results = result.get("research_results")
            investment_plan = result.get("investment_plan")
        else:
            portfolio_plan = getattr(result, "portfolio_plan", None)
            research_results = getattr(result, "research_results", None)
            investment_plan = getattr(result, "investment_plan", None)

        if portfolio_plan:
            print("Portfolio Allocation:")
            print("-" * 50)
            for company in portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * profile["investment_amount"]
                print(
                    f"{company['company_name']:<25} {allocation:>6.1f}% ${amount:>10,.2f}"
                )
            print("-" * 50)
            print(f"Total Allocation: {portfolio_plan['total_allocation']:.1f}%")

        print("\n" + "=" * 50)
        print("🔍 RESEARCH RESULTS")
        print("=" * 50)

        if research_results:
            for i, company in enumerate(research_results, 1):
                print(f"{i}. {company['name']}")
                print(f"   Risk: {company['risk_factor']}")
                print(f"   Reason: {company['explanation']}")
                print()

        print("\n" + "=" * 50)
        print("📋 FINAL INVESTMENT PLAN")
        print("=" * 50)

        if investment_plan:
            print(investment_plan)
        else:
            print("No investment plan generated.")

    except Exception as e:
        logger.error(f"Error generating investment plan: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
