"""Message classification endpoints"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import MessageInput, ClassificationOutput
from app.services.claude_service import ClaudeService

router = APIRouter()
claude_service = ClaudeService()

@router.post("/classify-message", response_model=ClassificationOutput)
async def classify_message(input: MessageInput):
    """Classify a chat message"""
    try:
        result = await claude_service.classify_message(input.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
