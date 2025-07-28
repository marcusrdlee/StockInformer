# StockInformer - AI Investment Planning Agent

Welcome to **StockInformer**! This project demonstrates how to create intelligent AI agents for personalized investment planning using Large Language Models (LLMs) and LangGraph. The system provides a **Personalized Investment Planning Agent** that can research companies, build optimal portfolios, generate investment rationale, and create professional investment reports.

## 🎯 What This Agent Does

The investment planning agent creates personalized investment portfolios based on:

- **Risk Level** (Low, Medium, High)
- **Industry Focus** (optional, e.g., "Big tech", "Healthcare")
- **Investment Amount** (e.g., $100,000)
- **Time Horizon** (e.g., "1 year", "5 years")

## 🔄 4-Step Investment Planning Process

### Step 1: Research Companies

- Uses SerpAPI to search for companies in the selected industry
- Identifies top 10 companies with strong market potential
- Analyzes risk factors and investment suitability

### Step 2: Build Portfolio Plan

- Creates optimal portfolio allocation based on research results
- Considers investor's risk tolerance and time horizon
- Allocates investment amount across selected companies

### Step 3: Generate Investment Rationale

- Provides detailed explanations for each selected company
- Explains why each company fits the investor's profile
- Includes risk assessment and growth potential analysis

### Step 4: Format Final Report

- Creates a professional Markdown investment plan
- Includes executive summary, portfolio table, and detailed analysis
- Provides recommendations and risk management strategies

## 🛠️ Key Technologies

- **LLM**: NVIDIA's Llama 3.3 70B Instruct model
- **Framework**: LangGraph for agent orchestration
- **Search**: SerpAPI for company research
- **Environment**: JupyterLab-based development environment

## 🚀 Quick Start

### Prerequisites

1. Python 3.8+
2. NVIDIA API key (for LLM access)
3. SerpAPI key (for company research)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp variables.env.example variables.env
# Edit variables.env with your API keys
```

### Usage Examples

#### Basic Usage

```python
from investment_agent import create_investment_plan

# Create a personalized investment plan
plan = create_investment_plan(
    risk_level="Medium",
    industry="Big tech",
    investment_amount=100000.0,
    time_horizon="1 year"
)

# Access the results
print(plan.investment_plan)  # Final report
print(plan.portfolio_plan)   # Portfolio allocation
print(plan.research_results) # Company research
```

#### Run Examples

```bash
# Test the agent functionality
python code/test_investment_agent.py

# Run example scenarios
python code/example_usage.py

# Run the full client
python code/investment_client.py
```

## 📁 Project Structure

```
StockInformer/
├── code/
│   ├── investment_agent/          # Core investment planning agent
│   │   ├── __init__.py           # Main entry point
│   │   ├── agent.py              # 4-step workflow implementation
│   │   ├── tools.py              # SerpAPI integration
│   │   └── prompts.py            # Specialized prompts for each step
│   ├── investment_client.py      # Main client script
│   ├── test_investment_agent.py  # Test script
│   └── example_usage.py          # Usage examples
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

- `NVIDIA_API_KEY`: Your NVIDIA API key for LLM access
- `SERPAPI_API_KEY`: Your SerpAPI key for company research
- `LANGSMITH_TRACING`: Enable LangSmith tracing (optional)

### Customization

- Modify prompts in `code/investment_agent/prompts.py`
- Add new tools in `code/investment_agent/tools.py`
- Adjust risk profiles and allocation strategies in the agent logic
