from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Financial DNA / Risk Profile
    risk_score = Column(String)  # Conservative, Balanced, Growth
    risk_profile_explanation = Column(String)

    financial_data = relationship("FinancialData", back_populates="user", uselist=False)
    goals = relationship("Goal", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class FinancialData(Base):
    __tablename__ = "financial_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Encrypted fields
    income = Column(String)  # AES-256 Encrypted
    expenses = Column(String) # AES-256 Encrypted
    debts = Column(String)    # AES-256 Encrypted
    savings = Column(String)  # AES-256 Encrypted

    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user = relationship("User", back_populates="financial_data")

class GoalType(str, enum.Enum):
    RETIREMENT = "retirement"
    HOME_PURCHASE = "home_purchase"
    EMERGENCY_FUND = "emergency_fund"
    EDUCATION = "education"
    OTHER = "other"

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    type = Column(Enum(GoalType), default=GoalType.OTHER)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="goals")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False) # e.g., "ai_recommendation", "goal_created"
    recommendation = Column(String)
    explanation = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
