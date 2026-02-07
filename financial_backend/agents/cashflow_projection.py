from typing import Dict, Any, List
from ..config import app
from ..utils import parse_json_response

def calculate_projection(income: float, expenses: float, months: int = 6) -> List[float]:
    surplus = income - expenses
    # Simple linear projection for now
    return [surplus] * months

@app.reasoner()
async def cashflow_projection(income: float, expenses: float) -> Dict[str, Any]:
    """
    Computes monthly surplus and generates a 6-month projection.
    Identifies risk periods.
    """
    
    # Use tool/skill for calculation
    projection_data = calculate_projection(income, expenses)
    monthly_surplus = income - expenses
    
    # Use AI to add context or identify risks (simulated "reasoning" about the numbers)
    response = await app.ai(
        system="""You are a cashflow expert API. Your ONLY job is to analyze data and return JSON.
        You are NOT a coding assistant. Do NOT write Python code.
        
        Given the calculated financial data, format the output and identify if there are any immediate risks based on the surplus.
        
        The projection is a flat list for 6 months.
        
        Return ONLY valid JSON:
        {
          "monthly_surplus": number,
          "projection": [number, number, ...],
          "risk_analysis": "string"
        }
        """,
        user=f"""
        Income: {income}
        Expenses: {expenses}
        Calculated Monthly Surplus: {monthly_surplus}
        Calculated Projection: {projection_data}
        """
    )
    
    result = parse_json_response(response)
    
    # Ensure the numbers match the calculation
    if isinstance(result, dict):
        result["monthly_surplus"] = monthly_surplus
        result["projection"] = projection_data
    else:
        result = {
            "monthly_surplus": monthly_surplus,
            "projection": projection_data,
            "risk_analysis": "Error parsing AI response"
        }
    
    return result
