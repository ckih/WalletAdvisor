from datetime import datetime
from typing import List, Dict
import math

def calculate_goal_roadmap(
    target_amount: float,
    current_amount: float,
    target_date: datetime,
    extra_monthly_savings: float = 0.0
) -> Dict:
    """
    Computes required monthly savings and a month-by-month roadmap.
    """
    now = datetime.utcnow()
    # Calculate months remaining
    months_remaining = (target_date.year - now.year) * 12 + (target_date.month - now.month)
    if months_remaining <= 0:
        months_remaining = 1

    remaining_amount = target_amount - current_amount
    if remaining_amount <= 0:
        return {
            "monthly_savings_required": 0.0,
            "roadmap": []
        }

    monthly_savings_required = remaining_amount / months_remaining

    roadmap = []
    temp_balance = current_amount
    for m in range(1, months_remaining + 1):
        # We simulate adding the required amount + any extra the user wants to test
        temp_balance += monthly_savings_required + extra_monthly_savings
        roadmap.append({
            "month": m,
            "target_savings": monthly_savings_required,
            "projected_balance": min(temp_balance, target_amount)
        })
        if temp_balance >= target_amount:
            break

    return {
        "monthly_savings_required": monthly_savings_required,
        "roadmap": roadmap
    }
