from typing import Dict, Any
from ..config import app
from ..utils import parse_json_response

@app.reasoner()
async def scenario_simulator(
    current_profile: Dict[str, Any],
    scenario: str,
    percentage: float
) -> Dict[str, Any]:
    """
    Simulates a financial scenario by modifying the profile.
    """
    
    response = await app.ai(
        system="""You are a financial simulator. Modify the financial profile based on the scenario.
        
        Scenarios:
        - "income_drop": Decrease income by percentage.
        - "expense_spike": Increase expenses by percentage.
        - "savings_increase": Increase savings by percentage.
        
        Return the modified profile in JSON:
        {
          "income": number,
          "expenses": number,
          "savings": number,
          "debt": number,
          "risk_tolerance": "string",
          "goal": "string",
          "simulation_note": "string explaining the change"
        }
        """,
        user=f"""
        Current Profile:
        {current_profile}
        
        Scenario: {scenario}
        Percentage Change: {percentage}%
        """
    )
    
    return parse_json_response(response)
