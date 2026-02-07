from .config import app
from .agents import orchestrator, profile_analyzer, cashflow_projection, allocation_planner, scenario_simulator, validator

# The app object is the Agent instance which inherits from FastAPI
# Importing the agents ensures the @app.reasoner decorators are executed and routes registered.

if __name__ == "__main__":
    app.serve(port=8002)
