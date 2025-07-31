"""Main entry point for the investment planning workflow."""

from typing import Any
from .agent import InvestmentAgentState, graph


async def create_investment_plan(
    risk_level: str,
    industry: str | None,
    investment_amount: float,
    time_horizon: str,
) -> Any | dict[str, Any] | None:
    """Create a personalized investment plan."""
    state = InvestmentAgentState(
        risk_level=risk_level,
        industry=industry,
        investment_amount=investment_amount,
        time_horizon=time_horizon,
    )
    result = await graph.ainvoke(state)
    return result
