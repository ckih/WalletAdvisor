import torch
import torch.nn as nn
from typing import Dict, Any, Tuple

class RiskScorer:
    """
    A rules-based risk scoring engine wrapped in a PyTorch-compatible interface.
    Phase 1: Rules-based.
    Phase 2: Can be replaced with a real PyTorch model.
    """
    def __init__(self):
        # Placeholder for PyTorch model if needed later
        self.model = None

    def predict(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        Computes risk score based on financial data.
        Returns: (score_category, explanation)
        """
        income = float(data.get("income", 0))
        expenses = float(data.get("expenses", 0))
        savings = float(data.get("savings", 0))
        debts = float(data.get("debts", 0))
        time_horizon = int(data.get("time_horizon", 5)) # Years
        risk_tolerance = int(data.get("risk_tolerance", 5)) # 1-10 scale

        # Simple logic for MVP
        disposable_income = income - expenses
        debt_to_income = debts / income if income > 0 else 1.0
        savings_ratio = savings / income if income > 0 else 0.0

        score = 0

        # Risk tolerance is a big factor
        score += risk_tolerance * 2

        # Time horizon factor
        if time_horizon > 10:
            score += 10
        elif time_horizon > 5:
            score += 5

        # Financial health factors
        if debt_to_income < 0.3:
            score += 5
        if savings_ratio > 0.2:
            score += 5

        # Determine category
        if score > 25:
            category = "Growth"
        elif score > 15:
            category = "Balanced"
        else:
            category = "Conservative"

        explanation = self.explain(data, category, score)
        return category, explanation

    def explain(self, data: Dict[str, Any], category: str, score: int) -> str:
        factors = []
        if int(data.get("risk_tolerance", 5)) > 7:
            factors.append("high stated risk tolerance")
        if int(data.get("time_horizon", 5)) > 10:
            factors.append("long investment time horizon")

        income = float(data.get("income", 0))
        debts = float(data.get("debts", 0))
        if income > 0 and (debts/income) < 0.3:
            factors.append("low debt-to-income ratio")

        factor_str = ", ".join(factors)
        return f"Your '{category}' profile (score: {score}) is based on your {factor_str}."

# Stub for Phase 2: Synthetic training script
def train_stub():
    """
    TODO: Phase 2 - Implement synthetic data generation and PyTorch model training.
    """
    pass
