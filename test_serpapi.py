#!/usr/bin/env python3
"""
Simple script to test SerpAPI key
"""

import os
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper

# Load environment variables
load_dotenv("secrets.env")

def test_serpapi():
    """Test if the SerpAPI key is working."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    print(f"SerpAPI Key found: {'Yes' if api_key else 'No'}")
    print(f"SerpAPI Key: {api_key}" if api_key else "No key")
    
    if not api_key or api_key == "your_serpapi_key_here":
        print("❌ No valid SerpAPI key found in secrets.env")
        print("Please get a free API key from https://serpapi.com/")
        return False
    
    try:
        # Test the API key
        serpapi = SerpAPIWrapper(serpapi_api_key=api_key)
        
        # Simple test search
        results = serpapi.run("Apple Inc stock")
        
        print("✅ SerpAPI Key is working!")
        print(f"Search results preview: {results[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ SerpAPI test failed: {e}")
        return False

if __name__ == "__main__":
    test_serpapi() 