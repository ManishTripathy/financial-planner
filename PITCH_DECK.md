# 🚀 AgentField Adaptive Financial Planner
## Hackathon Pitch & Technical Deep Dive

### 1. Project Overview
**What is it?**
The Adaptive Financial Planner is a multi-agent AI system built on **AgentField**. It doesn't just "chat" about money; it **reasons**, **calculates**, and **validates** financial strategies. It creates personalized financial plans and simulates "what-if" scenarios (like losing a job or getting a raise) to test plan resilience.

**Key Value Prop:**
*   **Orchestrated AI**: Multiple specialized agents work together (Analyzer -> Planner -> Validator).
*   **Safety First**: A dedicated "Risk Manager" agent validates every strategy before it reaches the user.
*   **Dynamic Simulation**: Adapts strategies in real-time based on simulated economic events.

---

### 2. Architecture & Components

The system is organized as a **Directed Acyclic Graph (DAG)** of reasoners, coordinated by a central Orchestrator.

#### 🧠 The Core Components

| Component | Type | Role | "The Persona" |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | `Reasoner` | **Conductor**. Manages the workflow, passes data between agents, and handles errors. | *The Project Manager* |
| **Profile Analyzer** | `Reasoner` | **Diagnostic**. Analyzes income, debt, and goals to determine "Financial Health" (Stable, Stressed, Growing). | *The Analyst* |
| **Cashflow Engine** | `Reasoner` | **Quantitative**. Calculates monthly surplus and projects cashflow 6 months out. Identifies liquidity risks. | *The Accountant* |
| **Allocation Planner** | `Reasoner` | **Strategic**. Takes analysis + cashflow and builds a plan (Emergency Fund, Investments, Debt Payoff). | *The Advisor* |
| **Strategy Validator** | `Reasoner` | **Quality Assurance**. Reviews the proposed plan against risk tolerance. Can **reject** unsafe advice. | *The Risk Officer* |
| **Scenario Simulator** | `Reasoner` | **Simulation**. Modifies the user's profile (e.g., -10% income) and triggers a re-planning cycle. | *The Stress Tester* |

#### 💾 Shared Memory
We use AgentField's shared state to maintain the user's "Financial Context" across different agents. This ensures the *Risk Officer* knows what the *Analyst* found without needing to re-read the raw data.

---

### 3. Live Demo Analysis

We ran two real-time API calls to demonstrate the system's reasoning capabilities.

#### 🎬 Scenario 1: The "Aggressive Grower"
**User Profile:**
*   **Income**: $6,000 | **Expenses**: $4,000
*   **Debt**: $5,000
*   **Goal**: Aggressive Growth | **Risk Tolerance**: High

**What Happened:**
1.  **Analyzer**: Labeled health as **"Growing"** (Income > Expenses). Identified constraints: "Debt: $5,000".
2.  **Cashflow**: Calculated a healthy **$2,000 monthly surplus**.
3.  **Planner**: Proposed an aggressive split:
    *   *Investments*: 60% of surplus into ETFs/Index Funds.
    *   *Debt*: Pay fixed amount monthly.
4.  **Validator (The Catch!)**: The Risk Officer **REJECTED** the plan (`is_valid: false`).
    *   *Reason*: "The proposed strategy lacks a clear plan for emergency fund replenishment."
    *   *Feedback*: Even aggressive investors need a safety net. The system caught the oversight!

**Verdict**: The system prioritized safety over the user's "aggressive" desire, preventing bad advice.

---

#### 🎬 Scenario 2: The "Expense Spike" Simulation
**Input**: Simulate a **20% spike in expenses** (Inflation? Rent hike?).

**What Happened:**
1.  **Simulator**:
    *   Modified Expenses: $4,000 -> **$4,800**.
    *   Updated Profile: Health check re-run.
2.  **Re-Analysis**:
    *   **Cashflow**: Surplus dropped from $2,000 -> **$1,200**.
3.  **Adapted Strategy**:
    *   *Previous*: 60% into Aggressive Growth.
    *   *New*: "Prioritize debt repayment... while maintaining an emergency fund."
4.  **Validator**: Still cautious (`is_valid: false`), warning that liquidity is now even tighter with higher expenses.

**Verdict**: The system successfully adapted to the new reality. It recognized the reduced surplus ($1,200) and shifted the focus from "Aggressive Growth" to "Debt Repayment & Survival".

---

### 4. Why This Matters
Most "Financial AI" is just a chatbot wrapper. This is an **Agentic System**:
1.  **It does Math**: Cashflow projections are calculated, not hallucinated.
2.  **It Self-Corrects**: The Validator agent acts as a guardrail.
3.  **It Adapts**: The Simulation engine proves the system can handle changing circumstances dynamically.

Refer to video here
