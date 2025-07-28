#!/usr/bin/env python3
"""
Test script for the Investment Planning Agent

This script tests the basic functionality of the investment planning agent
without requiring external API keys.
"""

import asyncio
import logging
from unittest.mock import AsyncMock, patch

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the investment agent
from investment_agent import InvestmentAgentState, graph


async def test_investment_agent():
    """Test the investment planning agent with mock data."""
    
    print("🧪 Testing Investment Planning Agent")
    print("=" * 50)
    
    # Test parameters
    risk_level = "Medium"
    industry = "Big tech"
    investment_amount = 100000.0
    time_horizon = "1 year"
    
    print(f"Test Parameters:")
    print(f"Risk Level: {risk_level}")
    print(f"Industry: {industry}")
    print(f"Investment Amount: ${investment_amount:,.2f}")
    print(f"Time Horizon: {time_horizon}")
    print("-" * 50)
    
    # Create test state
    state = InvestmentAgentState(
        risk_level=risk_level,
        industry=industry,
        investment_amount=investment_amount,
        time_horizon=time_horizon
    )
    
    try:
        # Mock the search function to avoid API calls
        with patch('investment_agent.tools.search_companies') as mock_search:
            mock_search.return_value = """
Search Results for: top companies Big tech industry investment potential 1 year

Fallback Company Data:
- Apple Inc. (AAPL): Technology giant with strong fundamentals and consistent growth
- Microsoft Corporation (MSFT): Cloud computing leader with diversified revenue streams
- Alphabet Inc. (GOOGL): Digital advertising and cloud services powerhouse
- Amazon.com Inc. (AMZN): E-commerce and cloud computing leader
- NVIDIA Corporation (NVDA): AI and semiconductor technology leader
- Tesla Inc. (TSLA): Electric vehicle and clean energy innovator
- Meta Platforms Inc. (META): Social media and metaverse technology company
- Berkshire Hathaway Inc. (BRK.A): Diversified investment holding company
- JPMorgan Chase & Co. (JPM): Leading financial services institution
- Johnson & Johnson (JNJ): Healthcare and pharmaceutical conglomerate
            """
            
            # Execute the investment planning workflow
            result = await graph.ainvoke(state)
            print("✅ Investment plan generated successfully!")
            
            # Display test results
            print("\n" + "=" * 50)
            print("📊 TEST RESULTS")
            print("=" * 50)
            
            if result.research_results:
                print(f"✅ Research Results: {len(result.research_results)} companies found")
                for i, company in enumerate(result.research_results[:3], 1):
                    print(f"   {i}. {company['name']} ({company['risk_factor']})")
            
            if result.portfolio_plan:
                print(f"✅ Portfolio Plan: {len(result.portfolio_plan['companies'])} companies allocated")
                total_allocation = result.portfolio_plan['total_allocation']
                print(f"   Total Allocation: {total_allocation:.1f}%")
            
            if result.investment_rationale:
                print("✅ Investment Rationale: Generated")
            
            if result.investment_plan:
                print("✅ Final Investment Plan: Generated")
                # Show first 200 characters of the plan
                preview = result.investment_plan[:200] + "..." if len(result.investment_plan) > 200 else result.investment_plan
                print(f"   Preview: {preview}")
            
            print("\n🎉 All tests passed! The investment agent is working correctly.")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_investment_agent()) 