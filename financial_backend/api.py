from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from .agents.orchestrator import orchestrate_strategy_generation, orchestrate_scenario_simulation, get_memory

app = FastAPI(title="Financial Planner Agent API")

class FinancialProfileRequest(BaseModel):
    income: float
    expenses: float
    savings: float
    debt: float
    risk_tolerance: str
    goal: str

class ScenarioRequest(BaseModel):
    scenario: str
    percentage: float

@app.post("/generate-strategy")
async def generate_strategy(profile: FinancialProfileRequest):
    try:
        # Convert Pydantic to dict
        profile_dict = profile.dict()
        result = await orchestrate_strategy_generation(profile_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate-scenario")
async def simulate_scenario(scenario: ScenarioRequest):
    try:
        scenario_dict = scenario.dict()
        result = await orchestrate_scenario_simulation(scenario_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory")
async def read_memory():
    return get_memory()

@app.get("/")
async def root():
    return {"message": "AgentField Financial Planner API is running"}
