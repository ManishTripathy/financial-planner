from typing import Dict, Any
from ..config import app
from ..utils import parse_json_response

@app.reasoner()
async def allocation_planner(
    profile_analysis: Dict[str, Any], 
    cashflow: Dict[str, Any],
    risk_tolerance: str
) -> Dict[str, Any]:
    """
    Generates the primary financial strategy based on analysis and cashflow.
    """
    
    response = await app.ai(
        system="""You are a financial planner API. Your ONLY job is to create a strategy and return JSON.
        You are NOT a coding assistant. Do NOT write Python code.
        
        Create a strategy based on the analysis and cashflow.
        
        Output ONLY valid JSON:
        {
          "emergency_fund": "recommendation string",
          "investment_strategy": "recommendation string",
          "debt_plan": "recommendation string"
        }
        """,
        user=f"""
        Financial Health: {profile_analysis.get('financial_health')}
        Constraints: {profile_analysis.get('constraints')}
        Priorities: {profile_analysis.get('priorities')}
        
        Monthly Surplus: {cashflow.get('monthly_surplus')}
        Risk Analysis: {cashflow.get('risk_analysis')}
        Risk Tolerance: {risk_tolerance}
        
        Provide specific recommendations for emergency fund, investments, and debt repayment.
        """
    )
    
    return parse_json_response(response)
