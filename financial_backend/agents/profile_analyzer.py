from typing import Dict, Any
from ..config import app
from ..utils import parse_json_response

@app.reasoner()
async def analyze_financial_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes the user's financial profile to determine health, constraints, and priorities.
    """
    
    response = await app.ai(
        system="""You are a financial analyst. Analyze the user's financial profile.
        Determine:
        1. Financial Health: "stable", "stressed", or "growing".
           - Stressed: Expenses > Income or High Debt.
           - Stable: Income >= Expenses but low savings.
           - Growing: High savings rate, low debt.
        2. Constraints: List of financial limitations.
        3. Priorities: List of financial goals to prioritize.
        
        Return the result in JSON format matching the schema:
        {
          "financial_health": "stable|stressed|growing",
          "constraints": ["string"],
          "priorities": ["string"]
        }
        """,
        user=f"""
        Income: {profile.get('income')}
        Expenses: {profile.get('expenses')}
        Savings: {profile.get('savings')}
        Debt: {profile.get('debt')}
        Risk Tolerance: {profile.get('risk_tolerance')}
        Goal: {profile.get('goal')}
        """
    )
    
    return parse_json_response(response)
