"""User analysis and moderation endpoints"""
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.models.schemas import UserBehaviorInput, TrustAnalysis, SellerModerationSettings
from app.services.user_analysis_service import UserAnalysisService

router = APIRouter()
user_service = UserAnalysisService()


@router.post("/analyze-user", response_model=TrustAnalysis)
async def analyze_user(input: UserBehaviorInput):
    """
    Analyze user trustworthiness and behavior.
    Uses run_in_threadpool to handle synchronous Anthropic API calls.
    """
    try:
        result = await run_in_threadpool(user_service.analyze_user, input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-user-allowed")
async def check_user_allowed(
    user_analysis: TrustAnalysis,
    moderation_settings: SellerModerationSettings
):
    """Check if user should be allowed based on seller settings"""
    allowed, reason = user_service.should_allow_interaction(
        user_analysis,
        moderation_settings
    )
    
    return {
        "allowed": allowed,
        "reason": reason,
        "trust_score": user_analysis.trust_score,
        "risk_level": user_analysis.risk_level
    }
