import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, FinancialData, Goal, AuditLog, GoalType
from app.core.security import get_password_hash
from app.core.config import settings, encryption_service

# Use the database URL from settings
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    try:
        # 1. Create a Demo User
        demo_user = db.query(User).filter(User.email == "demo@example.com").first()
        if not demo_user:
            demo_user = User(
                email="demo@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="Demo User",
                risk_score="Balanced",
                risk_profile_explanation="Your profile is balanced because you have a moderate risk tolerance and a medium-term time horizon."
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"Created user: {demo_user.email}")

        # 2. Add Financial Data
        fin_data = db.query(FinancialData).filter(FinancialData.user_id == demo_user.id).first()
        if not fin_data:
            fin_data = FinancialData(
                user_id=demo_user.id,
                income=encryption_service.encrypt("85000"),
                expenses=encryption_service.encrypt("45000"),
                savings=encryption_service.encrypt("15000"),
                debts=encryption_service.encrypt("5000")
            )
            db.add(fin_data)
            print("Added financial data")

        # 3. Add some Goals
        if not db.query(Goal).filter(Goal.user_id == demo_user.id).first():
            goals = [
                Goal(
                    user_id=demo_user.id,
                    name="Emergency Fund",
                    type=GoalType.EMERGENCY_FUND,
                    target_amount=20000,
                    current_amount=15000,
                    target_date=datetime.utcnow() + timedelta(days=180)
                ),
                Goal(
                    user_id=demo_user.id,
                    name="New Home",
                    type=GoalType.HOME_PURCHASE,
                    target_amount=100000,
                    current_amount=5000,
                    target_date=datetime.utcnow() + timedelta(days=365 * 5)
                ),
                Goal(
                    user_id=demo_user.id,
                    name="Retirement",
                    type=GoalType.RETIREMENT,
                    target_amount=1000000,
                    current_amount=50000,
                    target_date=datetime.utcnow() + timedelta(days=365 * 30)
                )
            ]
            db.add_all(goals)
            print("Added goals")

        # 4. Add some Audit Logs
        if not db.query(AuditLog).filter(AuditLog.user_id == demo_user.id).first():
            logs = [
                AuditLog(
                    user_id=demo_user.id,
                    action="ai_recommendation",
                    recommendation="How should I save for my home?",
                    explanation="Based on your Balanced profile, I recommend increasing your monthly savings by $200. This will allow you to reach your target 6 months earlier without significant lifestyle changes."
                )
            ]
            db.add_all(logs)
            print("Added audit logs")

        db.commit()
        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist (useful for local dev without migrations running)
    Base.metadata.create_all(bind=engine)
    seed()
