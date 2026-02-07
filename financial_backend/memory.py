from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class FinancialProfile(BaseModel):
    income: float
    expenses: float
    savings: float
    debt: float
    risk_tolerance: str # low, medium, high
    goal: str

class FinancialAnalysis(BaseModel):
    financial_health: str # stable, stressed, growing
    constraints: List[str]
    priorities: List[str]

class CashflowProjection(BaseModel):
    monthly_surplus: float
    projection: List[float] # 6-month projection

class Strategy(BaseModel):
    emergency_fund: str
    investment_strategy: str
    debt_plan: str

class Scenario(BaseModel):
    scenario: str # income_drop, expense_spike, savings_increase
    percentage: float
    timestamp: str

class SharedMemory(BaseModel):
    user_profile: Optional[FinancialProfile] = None
    analysis: Optional[FinancialAnalysis] = None
    cashflow_projection: Optional[CashflowProjection] = None
    current_strategy: Optional[Strategy] = None
    scenario_history: List[Scenario] = []

    def update(self, data: Dict[str, Any]):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
