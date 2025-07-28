"""Main entry point for the investment planning workflow.

This code is a simple example of how to use the investment planning workflow.
"""

import logging

from . import create_investment_plan

logging.basicConfig(level=logging.INFO)

# Example investment profile
result = create_investment_plan(
    risk_level="Medium",
    industry="Big tech",
    investment_amount=100000.0,
    time_horizon="1 year"
)

if result and result.investment_plan:
    print("\n" + "=" * 60)
    print("📊 PERSONALIZED INVESTMENT PLAN")
    print("=" * 60)
    print(result.investment_plan)
    print("=" * 60)
    
    # Also show portfolio summary
    if result.portfolio_plan:
        print("\n📈 PORTFOLIO ALLOCATION SUMMARY")
        print("-" * 40)
        for company in result.portfolio_plan["companies"]:
            allocation = company["allocation_percentage"]
            amount = (allocation / 100) * 100000
            print(f"{company['company_name']:<25} {allocation:>6.1f}% ${amount:>10,.2f}")
        print("-" * 40)
        print(f"Total Allocation: {result.portfolio_plan['total_allocation']:.1f}%")
else:
    print("❌ Failed to generate investment plan") 