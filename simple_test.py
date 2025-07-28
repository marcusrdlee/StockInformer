#!/usr/bin/env python3
"""
Simple test of the investment agent without external APIs
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("secrets.env")

def test_basic_functionality():
    """Test basic functionality without external APIs."""
    
    print("🧪 Simple Investment Agent Test")
    print("=" * 40)
    
    # Test 1: Check if modules can be imported
    try:
        from investment_agent import InvestmentAgentState
        print("✅ InvestmentAgentState imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Test 2: Check if we can create a state
    try:
        state = InvestmentAgentState(
            risk_level="Medium",
            industry="Big tech",
            investment_amount=100000.0,
            time_horizon="1 year"
        )
        print("✅ InvestmentAgentState created successfully")
        print(f"   Risk Level: {state.risk_level}")
        print(f"   Industry: {state.industry}")
        print(f"   Amount: ${state.investment_amount:,.2f}")
        print(f"   Time Horizon: {state.time_horizon}")
    except Exception as e:
        print(f"❌ State creation failed: {e}")
        return
    
    # Test 3: Check API keys
    nvidia_key = os.getenv("NVIDIA_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    
    print(f"\n🔑 API Keys Status:")
    print(f"   NVIDIA API Key: {'✅ Found' if nvidia_key and nvidia_key != 'your_nvidia_api_key_here' else '❌ Missing'}")
    print(f"   SerpAPI Key: {'✅ Found' if serpapi_key and serpapi_key != 'your_serpapi_key_here' else '❌ Missing'}")
    
    if nvidia_key and nvidia_key != 'your_nvidia_api_key_here':
        print("\n🎉 Basic setup is working!")
        print("To run the full agent, get a SerpAPI key from https://serpapi.com/")
    else:
        print("\n⚠️  You need to set up your API keys in secrets.env")

if __name__ == "__main__":
    test_basic_functionality() 