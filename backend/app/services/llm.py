import anthropic
from app.core.config import settings
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20240620"

    async def get_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Sends a prompt to the LLM and returns the text response.
        """
        if not settings.ANTHROPIC_API_KEY:
            return "MOCK AI RESPONSE: I am sorry, but the AI service is not configured. Please add an API key. (Recommendation: Save more for your goals!)"

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"

llm_service = LLMService()
