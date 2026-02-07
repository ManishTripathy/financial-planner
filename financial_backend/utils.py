import json
import re
from typing import Dict, Any, Union

def parse_json_response(response: Any) -> Dict[str, Any]:
    """
    Parses JSON from AI response, handling Markdown code blocks and MultimodalResponse objects.
    """
    print(f"DEBUG: parse_json_response called with type: {type(response)}", flush=True)
    text = ""
    
    # Try to get text content from MultimodalResponse or similar objects
    if hasattr(response, "content"):
        text = str(response.content)
    elif hasattr(response, "text"):
        text = str(response.text)
    elif isinstance(response, dict):
        if "content" in response:
             text = str(response["content"])
        else:
             # It's already a dict and no content field to parse, so return it
             return dict(response)
    else:
        text = str(response)
        
    print(f"DEBUG: Extracted text: {text[:100]}...", flush=True)
    
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```', '', text)
    text = text.strip()
    
    try:
        return json.loads(text)
    except Exception as e:
        print(f"DEBUG: JSON parse failed: {e}", flush=True)
        return {"error": "Failed to parse", "raw": text}
