# AgentField Adaptive Financial Planner

This project is an **Adaptive Financial Planner** built using the **AgentField** framework. It orchestrates multiple AI agents (Reasoners) to analyze financial profiles, project cashflows, plan allocations, and simulate economic scenarios.

## Project Structure

The project is organized as a Python package `financial_backend` with the following key components:

### 1. Agents (Reasoners)
Located in `financial_backend/agents/`:
*   **Profile Analyzer** (`profile_analyzer.py`): Analyzes a user's financial inputs (income, expenses, debt, etc.) to determine financial health (stable, stressed, growing), identify constraints, and set priorities.
*   **Cashflow Projection** (`cashflow_projection.py`): Computes monthly surplus and projects cashflow over a 6-month period using both deterministic calculation and AI reasoning for risk identification.
*   **Allocation Planner** (`allocation_planner.py`): Generates actionable financial strategies (emergency fund, investments, debt repayment) based on the profile analysis and cashflow projections.
*   **Scenario Simulator** (`scenario_simulator.py`): Simulates the impact of financial events (e.g., "income_drop", "expense_spike") on the user's profile.
*   **Strategy Validator** (`validator.py`): Acts as a risk manager to validate proposed strategies against the user's risk tolerance and financial reality.
*   **Orchestrator** (`orchestrator.py`): The central coordinator that manages the workflow:
    1.  Receives user data.
    2.  Calls Profile Analyzer.
    3.  Calls Cashflow Projection.
    4.  Calls Allocation Planner.
    5.  Calls Strategy Validator.
    6.  Aggregates results.

### 2. Core Infrastructure
*   **API** (`financial_backend/api.py`): A FastAPI application exposing endpoints to interact with the system.
*   **Config** (`financial_backend/config.py`): Configures the AgentField app and LLM provider (using local Ollama by default).
*   **Memory** (`financial_backend/memory.py`): Defines the shared state models using Pydantic.
*   **Utils** (`financial_backend/utils.py`): Helper functions for robust JSON parsing from AI responses.

## Getting Started

### Prerequisites
*   **Docker & Docker Compose**
*   **Ollama**: Installed locally and running with the `llama3.2` model pulled (`ollama pull llama3.2`).

### Running with Docker Compose

1.  **Start the services**:
    ```bash
    docker-compose up --build
    ```
    This will start:
    *   `agentfield-server`: The AgentField control plane (port 8080).
    *   `financial-backend`: The Financial Planner API (port 8002).

2.  **Verify Status**:
    Check if the API is running:
    ```bash
    curl http://localhost:8002/
    ```
    Expected output: `{"message": "AgentField Financial Planner API is running"}`

## Usage & Testing

You can interact with the agent using `curl` commands.

### 1. Generate Financial Strategy
Send a user profile to generate a comprehensive financial plan.

```bash
curl -X POST http://localhost:8002/generate-strategy \
  -H "Content-Type: application/json" \
  -d '{
    "income": 5000,
    "expenses": 3500,
    "savings": 10000,
    "debt": 2000,
    "risk_tolerance": "medium",
    "goal": "long-term growth"
  }'
```

**Response includes:**
*   `profile_analysis`: Financial health assessment.
*   `cashflow`: 6-month projection and surplus calculation.
*   `strategy`: Recommendations for emergency fund, investments, and debt.
*   `validation`: Risk manager's approval or feedback.

### 2. Simulate Scenario (Stub)
Simulate a financial shock (e.g., income drop).

```bash
curl -X POST http://localhost:8002/simulate-scenario \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "income_drop",
    "percentage": 10
  }'
```

## Development

To run locally without Docker:

1.  **Create venv**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies**:
    ```bash
    pip install -e .
    ```
3.  **Run Server**:
    ```bash
    uvicorn financial_backend.api:app --host 0.0.0.0 --port 8002
    ```
