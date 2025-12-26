"""Claude API service"""
import json
from anthropic import Anthropic
from app.config import settings
from app.models.schemas import ClassificationOutput, GenerateOutput, ProductContext, SellerPreferences

class ClaudeService:
    """Service for Claude API interactions"""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
    
    async def classify_message(self, message: str) -> ClassificationOutput:
        """Classify a chat message"""
        prompt = f"""Analyze this live stream chat message.

Message: "{message}"

Respond with ONLY valid JSON:
{{
    "type": "question|comment|spam",
    "confidence": 0.0-1.0,
    "topic": "authenticity|pricing|specs|condition|shipping|general|other",
    "urgency": "high|medium|low",
    "reasoning": "brief explanation"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            
            return ClassificationOutput(
                type=result["type"],
                confidence=result["confidence"],
                topic=result.get("topic"),
                urgency=result.get("urgency", "medium"),
                reasoning=result["reasoning"]
            )
        except Exception as e:
            return ClassificationOutput(
                type="comment",
                confidence=0.5,
                reasoning=f"Error: {str(e)}"
            )
    
    async def generate_response(
        self,
        question: str,
        product_context: ProductContext,
        seller_preferences: SellerPreferences
    ) -> GenerateOutput:
        """Generate a response to buyer's question"""
        prompt = f"""You are helping a watch dealer respond to questions.

PRODUCT:
{product_context.model_dump_json(indent=2)}

QUESTION: "{question}"

Generate a {seller_preferences.tone} response (max {seller_preferences.max_length} chars).

Respond with ONLY valid JSON:
{{
    "response_text": "the response",
    "confidence": 0.0-1.0,
    "requires_review": true/false,
    "reasoning": "explanation"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            
            return GenerateOutput(
                response_text=result["response_text"],
                confidence=result["confidence"],
                requires_review=result["requires_review"],
                reasoning=result["reasoning"]
            )
        except Exception as e:
            return GenerateOutput(
                response_text="Let me check on that.",
                confidence=0.0,
                requires_review=True,
                reasoning=f"Error: {str(e)}"
            )
