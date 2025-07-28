#!/usr/bin/env python3
"""
Simple script to test NVIDIA API key
"""

import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Load environment variables
load_dotenv("secrets.env")

def test_nvidia_api():
    """Test if the NVIDIA API key is working."""
    
    api_key = os.getenv("NVIDIA_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    print(f"API Key starts with: {api_key[:10]}..." if api_key else "No key")
    
    if not api_key:
        print("❌ No NVIDIA API key found in secrets.env")
        return False
    
    try:
        # Test the API key
        llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)
        
        # Simple test message
        response = llm.invoke("Say 'Hello, API key is working!'")
        
        print("✅ API Key is working!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ API Key test failed: {e}")
        return False

if __name__ == "__main__":
    test_nvidia_api() 