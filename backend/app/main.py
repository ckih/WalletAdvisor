from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, risk, goals, chat

app = FastAPI(title="Autonomous Financial Adviser (AFA) API")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Welcome to AFA API"}
