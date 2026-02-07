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
    
    # For demo simplicity, we assume the profile is passed in or we have it.
    # If we don't have it in memory (stateless request), we might need it in input.
    # But let's assume it's in memory or we error out.
    # current_profile = memory.user_profile
    # For this demo, we'll return a mock or require profile in input if memory is empty.
    
    return {"message": "Scenario simulation not fully implemented in demo orchestrator yet."}

def get_memory():
    return memory.dict()
