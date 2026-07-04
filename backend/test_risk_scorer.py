import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.risk_scorer import RiskScorer

def test_risk_scorer():
    scorer = RiskScorer()

    # Growth profile
    growth_data = {
        "income": 10000,
        "expenses": 5000,
        "savings": 20000,
        "debts": 1000,
        "time_horizon": 15,
        "risk_tolerance": 8
    }
    category, explanation = scorer.predict(growth_data)
    print(f"Growth test: {category} - {explanation}")
    assert category == "Growth"

    # Conservative profile
    cons_data = {
        "income": 3000,
        "expenses": 2800,
        "savings": 500,
        "debts": 5000,
        "time_horizon": 2,
        "risk_tolerance": 2
    }
    category, explanation = scorer.predict(cons_data)
    print(f"Conservative test: {category} - {explanation}")
    assert category == "Conservative"

    print("Risk Scorer tests passed!")

if __name__ == "__main__":
    test_risk_scorer()
