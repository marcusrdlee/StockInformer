#!/usr/bin/env python3
"""
Simple test that shows results from the first two steps
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv("secrets.env")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Import the investment agent
from investment_agent import InvestmentAgentState, graph

async def simple_test():
    """Test the first two steps of the investment planning agent."""
    
    print("🧪 Simple Investment Agent Test")
    print("=" * 50)
    
    # Investment Profile
    risk_level = "Medium"
    industry = "Big tech"
    investment_amount = 100000.0
    time_horizon = "1 year"
    
    print(f"Risk Level: {risk_level}")
    print(f"Industry: {industry}")
    print(f"Investment Amount: ${investment_amount:,.2f}")
    print(f"Time Horizon: {time_horizon}")
    print("-" * 50)
    
    # Create investment plan
    state = InvestmentAgentState(
        risk_level=risk_level,
        industry=industry,
        investment_amount=investment_amount,
        time_horizon=time_horizon
    )
    
    try:
        # Execute just the first two steps manually
        print("Step 1: Researching companies...")
        from investment_agent.agent import step_1_research_companies
        state = await step_1_research_companies(state, {})
        
        print(f"Step 1 results: {state.research_results}")
        
        print("Step 2: Building portfolio...")
        from investment_agent.agent import step_2_build_portfolio
        state = await step_2_build_portfolio(state, {})
        
        print(f"Step 2 results: {state.portfolio_plan}")
        
        print("✅ First two steps completed successfully!")
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 RESEARCH RESULTS")
        print("=" * 50)
        
        if state.research_results:
            for i, company in enumerate(state.research_results, 1):
                print(f"{i}. {company['name']}")
                print(f"   Risk: {company['risk_factor']}")
                print(f"   Reason: {company['explanation']}")
                print()
        
        print("\n" + "=" * 50)
        print("📈 PORTFOLIO PLAN")
        print("=" * 50)
        
        if state.portfolio_plan:
            print("Portfolio Allocation:")
            print("-" * 50)
            for company in state.portfolio_plan["companies"]:
                allocation = company["allocation_percentage"]
                amount = (allocation / 100) * investment_amount
                print(f"{company['company_name']:<25} {allocation:>6.1f}% ${amount:>10,.2f}")
            print("-" * 50)
            print(f"Total Allocation: {state.portfolio_plan['total_allocation']:.1f}%")
        
        print("\n🎉 Investment planning pipeline is working!")
        print("The agent successfully researched companies and created a portfolio plan.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(simple_test()) 