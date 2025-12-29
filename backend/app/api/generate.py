"""Response generation endpoints"""
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.models.schemas import GenerateInput, GenerateOutput
from app.services.claude_service import ClaudeService

router = APIRouter()
claude_service = ClaudeService()

@router.post("/generate-response", response_model=GenerateOutput)
async def generate_response(input: GenerateInput):
    """Generate AI response to question"""
    try:
        result = await run_in_threadpool(
            claude_service.generate_response,
            input.question,
            input.product_context,
            input.seller_preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
