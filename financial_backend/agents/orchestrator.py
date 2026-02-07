from typing import Dict, Any
from ..config import app
from ..memory import SharedMemory
from .profile_analyzer import analyze_financial_profile
from .cashflow_projection import cashflow_projection
from .allocation_planner import allocation_planner
from .scenario_simulator import scenario_simulator
from .validator import strategy_validator

# Global memory instance for this demo (single user assumption)
memory = SharedMemory()

@app.reasoner()
async def orchestrate_strategy_generation(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates the full financial planning flow.
    """
    print("🚀 Starting Strategy Generation...", flush=True)
    
    # 1. Update Memory with User Profile
    # Simplified: Storing raw dict for flexibility in this demo, 
    # though SharedMemory defines fields as Pydantic models.
    # memory.user_profile = FinancialProfile(**profile) 
    # For now, let's just use local variable flow, and set memory at the end or if needed.
    
    # 2. Profile Analysis
    print("📊 Running Profile Analyzer...", flush=True)
    try:
        analysis = await analyze_financial_profile(profile)
        print(f"DEBUG: Analysis result type: {type(analysis)}", flush=True)
        # memory.analysis = analysis
    except Exception as e:
        print(f"ERROR in Profile Analyzer: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise e
    
    # 3. Cashflow Projection
    print("💰 Running Cashflow Projection...", flush=True)
    try:
        cashflow = await cashflow_projection(profile.get('income', 0), profile.get('expenses', 0))
        print(f"DEBUG: Cashflow result type: {type(cashflow)}", flush=True)
        # memory.cashflow_projection = cashflow
    except Exception as e:
        print(f"ERROR in Cashflow Projection: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise e
    
    # 4. Allocation Planner
    print("📝 Running Allocation Planner...", flush=True)
    try:
        strategy = await allocation_planner(analysis, cashflow, profile.get('risk_tolerance', 'medium'))
        # memory.current_strategy = strategy
    except Exception as e:
        print(f"ERROR in Allocation Planner: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise e
    
    # 5. Strategy Validator
    print("✅ Running Strategy Validator...", flush=True)
    try:
        validation = await strategy_validator(profile, strategy)
    except Exception as e:
        print(f"ERROR in Strategy Validator: {e}", flush=True)
        # Don't fail the whole request for validation error, just log
        validation = {"error": str(e)}
    
    result = {
        "strategy": strategy,
        "validation": validation,
        "analysis": analysis,
        "cashflow": cashflow
    }
    
    return result

@app.reasoner()
async def orchestrate_scenario_simulation(scenario_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates scenario simulation and strategy adaptation.
    """
    print("⚠️ Starting Scenario Simulation...", flush=True)
    
    scenario = scenario_input.get("scenario")
    percentage = scenario_input.get("percentage")
    profile = scenario_input.get("profile")

    if not profile:
        return {"error": "Missing 'profile' in input. Please provide the current financial profile."}
    
    if not scenario:
         return {"error": "Missing 'scenario' in input."}

    # 1. Simulate Scenario
    print(f"🔄 Simulating scenario: {scenario} ({percentage}%)", flush=True)
    try:
        simulated_profile = await scenario_simulator(profile, scenario, percentage)
        print("✅ Simulation complete.", flush=True)
    except Exception as e:
        print(f"ERROR in Scenario Simulator: {e}", flush=True)
        return {"error": str(e)}

    # 2. Re-run Strategy Generation on new profile
    print("🔄 Generating adapted strategy...", flush=True)
    try:
        # Recursively call the strategy generation orchestrator
        # Since it is a reasoner, we can call it directly and it will execute
        new_strategy_result = await orchestrate_strategy_generation(simulated_profile)
    except Exception as e:
        print(f"ERROR in Strategy Generation during simulation: {e}", flush=True)
        return {"error": str(e)}
    
    return {
        "scenario_applied": f"{scenario} ({percentage}%)",
        "original_profile": profile,
        "simulated_profile": simulated_profile,
        "adapted_strategy_result": new_strategy_result
    }

def get_memory():
    return memory.dict()
