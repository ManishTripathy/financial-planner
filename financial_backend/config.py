import os
from agentfield import Agent, AIConfig

# Configuration for local Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "ollama/llama3.2")

litellm_params = {
    "drop_params": True,
    "api_base": OLLAMA_BASE_URL
}

ai_config = AIConfig(
    model=DEFAULT_MODEL,
    temperature=0.0, # Deterministic for financial calculations
    max_tokens=2048,
    litellm_params=litellm_params,
)

# Initialize AgentField app
app = Agent(
    node_id="financial_planner_backend",
    version="0.1.0",
    dev_mode=True,
    ai_config=ai_config,
)
