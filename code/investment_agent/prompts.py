"""
Prompts for the investment planning agent.
"""

from typing import Final

# Step 1: Company Research Prompt
company_research_prompt: Final[str] = """
You are an expert investment analyst. Your goal is to analyze search results and identify the top 10 companies suitable for investment.

Industry Focus: {industry}
Risk Level: {risk_level}
Time Horizon: {time_horizon}

Search Results:
{search_results}

Based on the search results above, identify the top 10 companies that would be suitable for a {risk_level} risk investor with a {time_horizon} investment horizon in the {industry} industry.

For each company, provide:
1. Company name (full legal name)
2. Risk factor (Low, Medium, or High)
3. Explanation of why this company might be a good investment for the specified risk profile and time horizon

Focus on companies with:
- Strong market position and competitive advantages
- Consistent financial performance
- Growth potential aligned with the time horizon
- Risk profile appropriate for the investor's risk tolerance
- Industry relevance and future prospects

Return exactly 10 companies, prioritizing quality over quantity if fewer than 10 suitable companies are found.

Return the companies as a list in the 'companies' field.
"""

# Step 2: Portfolio Planning Prompt
portfolio_planning_prompt: Final[str] = """
You are an expert portfolio manager. Your goal is to create an optimal portfolio allocation based on the researched companies and investor profile.

Available Companies:
{companies}

Investor Profile:
- Risk Level: {risk_level}
- Investment Amount: ${investment_amount:,.2f}
- Time Horizon: {time_horizon}

Create a portfolio plan that:
1. Selects the most suitable companies from the research results (not necessarily all 10)
2. Allocates the total investment amount across selected companies
3. Considers the investor's risk tolerance and time horizon
4. Provides optional holding periods for each stock

Portfolio Guidelines:
- For Low Risk: Focus on stable, dividend-paying companies with 60-80% allocation to large caps
- For Medium Risk: Balanced mix with 40-60% in growth stocks and 40-60% in value stocks
- For High Risk: Higher allocation to growth and emerging companies with 70-90% in growth stocks
- Ensure total allocation equals 100% of the investment amount
- Consider diversification across different market caps and sectors

Return a structured portfolio plan with company allocations and holding periods.
"""

# Step 3: Investment Rationale Prompt
investment_rationale_prompt: Final[str] = """
You are an expert investment advisor. Your goal is to explain the investment rationale for each company in the portfolio.

Portfolio Plan:
{portfolio_plan}

Research Results:
{research_results}

Investor Profile:
- Risk Level: {risk_level}
- Industry Focus: {industry}
- Time Horizon: {time_horizon}

For each company in the portfolio, provide a detailed explanation that includes:

1. **Company Overview**: Brief description of the company's business model and market position
2. **Investment Thesis**: Why this company fits the investor's profile
3. **Risk Assessment**: How the company's risk profile aligns with the investor's risk tolerance
4. **Growth Potential**: Expected performance over the specified time horizon
5. **Market Position**: Competitive advantages and industry positioning
6. **Financial Health**: Key financial metrics and stability indicators

Focus on explaining:
- How each company's characteristics match the investor's risk level
- Why the allocation percentage is appropriate for this investor
- How the time horizon affects the investment decision
- Industry-specific factors that make this company suitable

Write in a clear, professional tone suitable for an investment report.
"""

# Step 4: Final Report Formatting Prompt
final_report_prompt: Final[str] = """
You are an expert financial advisor creating a professional investment plan report.

Portfolio Plan:
{portfolio_plan}

Investment Rationale:
{investment_rationale}

Client Profile:
- Risk Level: {risk_level}
- Industry Focus: {industry}
- Investment Amount: ${investment_amount:,.2f}
- Time Horizon: {time_horizon}

Create a comprehensive, professional investment plan report in Markdown format that includes:

## Executive Summary
- Brief overview of the investment strategy
- Key highlights of the portfolio allocation
- Expected outcomes for the specified time horizon

## Portfolio Allocation Table
Create a clean table showing:
- Company Name
- Allocation Percentage
- Dollar Amount
- Holding Period (if specified)
- Risk Level

## Detailed Investment Analysis
For each company in the portfolio:
- Company overview and business model
- Investment thesis and rationale
- Risk assessment and mitigation
- Growth potential and market position
- Expected performance over the time horizon

## Risk Management
- Overall portfolio risk assessment
- Diversification analysis
- Risk mitigation strategies

## Recommendations
- Key actions for the investor
- Monitoring and rebalancing suggestions
- Exit strategy considerations

Format the report professionally with:
- Clear headings and subheadings
- Well-structured tables
- Bullet points for key information
- Professional language suitable for investment clients
- Proper Markdown formatting

Make the report comprehensive yet easy to understand for a retail investor.
""" 