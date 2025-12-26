"""Response generation endpoints"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateInput, GenerateOutput
from app.services.claude_service import ClaudeService

router = APIRouter()
claude_service = ClaudeService()

@router.post("/generate-response", response_model=GenerateOutput)
async def generate_response(input: GenerateInput):
    """Generate AI response to question"""
    try:
        result = await claude_service.generate_response(
            question=input.question,
            product_context=input.product_context,
            seller_preferences=input.seller_preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
