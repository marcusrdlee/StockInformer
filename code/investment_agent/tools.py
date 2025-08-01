"""Tools for the investment planning workflow."""

import os
import logging
from typing import Any

from langchain_community.utilities import SerpAPIWrapper

_LOGGER = logging.getLogger(__name__)


async def search_companies(query: str) -> str:
    """
    Search for companies using SerpAPI.

    Args:
        query: Search query for company research

    Returns:
        Formatted search results as string

    Raises:
        RuntimeError: If the search fails
    """
    _LOGGER.info("Searching for companies with query: %s", query)

    # Use SerpAPI to search for companies
    serpapi = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

    results = serpapi.run(query)

    # Format the results for better processing
    formatted_results = f"""
Search Results for: {query}

{results}

Please analyze these results to identify top companies suitable for investment.
Focus on companies with strong market position, growth potential, and financial stability.
    """

    return formatted_results


async def get_market_data(symbol: str) -> dict[str, Any]:
    """
    Get market data for a specific stock symbol.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')

    Returns:
        Dictionary containing market data

    Raises:
        RuntimeError: If market data cannot be fetched
    """
    _LOGGER.info("Getting market data for symbol: %s", symbol)

    # This would typically integrate with a financial data API
    # For now, return mock data
    mock_data = {
        "symbol": symbol,
        "price": 150.00,
        "change": 2.50,
        "change_percent": 1.67,
        "market_cap": "2.5T",
        "pe_ratio": 25.5,
        "volume": "50M",
    }

    return mock_data


async def analyze_risk_profile(company_name: str, industry: str) -> dict[str, Any]:
    """
    Analyze risk profile for a specific company.

    Args:
        company_name: Name of the company
        industry: Industry sector

    Returns:
        Dictionary containing risk analysis
    """
    try:
        _LOGGER.info("Analyzing risk profile for: %s in %s", company_name, industry)

        # This would typically use financial analysis APIs
        # For now, return mock risk analysis
        risk_profiles = {
            "Apple Inc.": {
                "risk_level": "Low",
                "factors": ["Strong cash flow", "Brand loyalty", "Diversified revenue"],
            },
            "Microsoft Corporation": {
                "risk_level": "Low",
                "factors": ["Cloud leadership", "Enterprise focus", "Stable growth"],
            },
            "Tesla Inc.": {
                "risk_level": "High",
                "factors": ["Volatile stock", "Competition", "Regulatory risks"],
            },
            "NVIDIA Corporation": {
                "risk_level": "Medium",
                "factors": ["AI growth", "Chip demand", "Market volatility"],
            },
        }

        return risk_profiles.get(
            company_name,
            {
                "risk_level": "Medium",
                "factors": [
                    "Market conditions",
                    "Industry trends",
                    "Company fundamentals",
                ],
            },
        )

    except Exception as e:
        _LOGGER.error("Error analyzing risk for %s: %s", company_name, str(e))
        return {"risk_level": "Unknown", "factors": ["Unable to analyze risk profile"]}
