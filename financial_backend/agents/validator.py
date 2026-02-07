from typing import Dict, Any
from ..config import app
from ..utils import parse_json_response

@app.reasoner()
async def strategy_validator(
    profile: Dict[str, Any],
    strategy: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validates the proposed strategy against the profile.
    """
    
    response = await app.ai(
        system="""You are a risk manager API. Your ONLY job is to validate strategies and return JSON.
        You are NOT a coding assistant. Do NOT write Python code.
        
        Validate the proposed financial strategy.
        Check for:
        1. Liquidity safety (is there enough emergency fund?)
        2. Risk consistency (does investment match risk tolerance?)
        3. Logical contradictions.
        
        Output ONLY valid JSON:
        {
          "is_valid": boolean,
          "feedback": "string",
          "suggested_corrections": "string or null"
        }
        """,
        user=f"""
        User Profile: {profile}
        Proposed Strategy: {strategy}
        """
    )
    
    return parse_json_response(response)
