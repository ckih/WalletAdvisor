from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.risk import get_current_user
from app.models.models import User, FinancialData, Goal, AuditLog
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm import llm_service
from app.core.config import encryption_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Gather Context
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    financials = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).first()

    context = {
        "user_name": current_user.full_name,
        "risk_profile": current_user.risk_score,
        "goals": [{"name": g.name, "target": g.target_amount, "current": g.current_amount} for g in goals],
    }

    if financials:
        context["income"] = encryption_service.decrypt(financials.income)
        context["expenses"] = encryption_service.decrypt(financials.expenses)
        context["savings"] = encryption_service.decrypt(financials.savings)
        context["debts"] = encryption_service.decrypt(financials.debts)

    # 2. Construct System Prompt
    system_prompt = f"""
    You are an Autonomous Financial Adviser (AFA).
    User Context: {context}

    Guidelines:
    - Provide helpful financial advice based on the user's specific context.
    - Every recommendation must include a clear, plain-language explanation ("we suggest X because Y").
    - Be conversational but professional.
    - IMPORTANT: Include a disclaimer that this is not licensed financial advice.
    - Do not offer to execute transactions.
    """

    # 3. Get AI Response
    ai_response = await llm_service.get_response(request.message, system_prompt)

    # 4. Create Audit Log
    audit = AuditLog(
        user_id=current_user.id,
        action="ai_recommendation",
        recommendation=request.message,
        explanation=ai_response
    )
    db.add(audit)
    db.commit()

    return {
        "response": ai_response,
        "explanation": "Recommendation generated based on your financial DNA and current goals."
    }
