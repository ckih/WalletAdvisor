from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.core.deps import get_db
from app.core.config import settings
from app.models.models import User, FinancialData
from app.schemas.risk import OnboardingRequest, RiskProfileResponse
from app.services.risk_scorer import RiskScorer
from app.services.events import event_producer
from app.core.config import encryption_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
risk_scorer = RiskScorer()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/onboarding", response_model=RiskProfileResponse)
async def onboarding(
    data: OnboardingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Compute Risk Score
    category, explanation = risk_scorer.predict(data.model_dump())

    # 2. Update User Risk Profile
    current_user.risk_score = category
    current_user.risk_profile_explanation = explanation

    # 3. Encrypt and save financial data
    financial_data = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()
    if not financial_data:
        financial_data = FinancialData(user_id=current_user.id)
        db.add(financial_data)

    financial_data.income = encryption_service.encrypt(str(data.income))
    financial_data.expenses = encryption_service.encrypt(str(data.expenses))
    financial_data.savings = encryption_service.encrypt(str(data.savings))
    financial_data.debts = encryption_service.encrypt(str(data.debts))

    db.commit()

    # 4. Emit Event
    event_producer.emit("risk_profile_updated", {
        "user_id": current_user.id,
        "category": category,
        "timestamp": str(current_user.created_at)
    })

    return {"category": category, "explanation": explanation}

@router.get("/profile", response_model=RiskProfileResponse)
async def get_risk_profile(current_user: User = Depends(get_current_user)):
    if not current_user.risk_score:
        raise HTTPException(status_code=404, detail="Risk profile not found. Please complete onboarding.")
    return {
        "category": current_user.risk_score,
        "explanation": current_user.risk_profile_explanation
    }
