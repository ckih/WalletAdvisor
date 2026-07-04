from pydantic import BaseModel
from typing import Optional

class OnboardingRequest(BaseModel):
    income: float
    expenses: float
    savings: float
    debts: float
    time_horizon: int
    risk_tolerance: int

class RiskProfileResponse(BaseModel):
    category: str
    explanation: str

    class Config:
        from_attributes = True
