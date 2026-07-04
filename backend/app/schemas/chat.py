from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    explanation: str # Every recommendation must have an explanation
