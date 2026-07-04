import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.financial_math import calculate_goal_roadmap

def test_financial_math():
    target = 12000
    current = 0
    target_date = datetime.utcnow() + timedelta(days=365) # 12 months roughly

    result = calculate_goal_roadmap(target, current, target_date)
    print(f"Monthly savings required: {result['monthly_savings_required']}")
    assert 950 < result['monthly_savings_required'] < 1050
    assert len(result['roadmap']) >= 11

    # What-if scenario
    result_extra = calculate_goal_roadmap(target, current, target_date, extra_monthly_savings=1000)
    print(f"Roadmap length with extra savings: {len(result_extra['roadmap'])}")
    assert len(result_extra['roadmap']) < len(result['roadmap'])

    print("Financial math tests passed!")

if __name__ == "__main__":
    test_financial_math()
