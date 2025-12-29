"""Pydantic models for request/response schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class MessageInput(BaseModel):
    """Input for message classification"""
    message: str = Field(..., min_length=1, max_length=500)
    username: Optional[str] = None

class ClassificationOutput(BaseModel):
    """Output for message classification"""
    type: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    topic: Optional[str] = None
    urgency: Optional[str] = "medium"
    reasoning: str

class ProductContext(BaseModel):
    """Product information context"""
    brand: str
    model: str
    reference: Optional[str] = None
    price: float
    year: Optional[int] = None
    condition: str = "Not specified"
    movement: Optional[str] = None
    box_papers: bool = False

class SellerPreferences(BaseModel):
    """Seller communication preferences"""
    tone: str = "professional"
    max_length: int = 150
    include_username: bool = True

class GenerateInput(BaseModel):
    """Input for response generation"""
    question: str
    product_context: ProductContext
    seller_preferences: Optional[SellerPreferences] = SellerPreferences()

class GenerateOutput(BaseModel):
    """Output for response generation"""
    response_text: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    requires_review: bool
    reasoning: str
    alternative_responses: Optional[list[str]] = None
# User Analysis Models
class UserBehaviorInput(BaseModel):
    """Input for analyzing user behavior"""
    username: str
    message: str
    message_history: Optional[list[str]] = []
    account_age_days: Optional[int] = None
    previous_purchases: Optional[int] = 0
    is_verified: Optional[bool] = False
    follower_count: Optional[int] = None
    following_count: Optional[int] = None

class TrustAnalysis(BaseModel):
    """Output of user trust analysis"""
    username: str
    trust_score: float = Field(..., ge=0.0, le=100.0)
    classification: str
    risk_level: str
    flags: list[str] = []
    reasoning: str
    recommended_action: str
    
class SellerModerationSettings(BaseModel):
    """Seller's moderation preferences"""
    require_verification: bool = False
    auto_block_bots: bool = True
    auto_block_trolls: bool = True
    min_trust_score: int = 30
    allow_new_accounts: bool = True
    min_account_age_days: int = 0
    alert_on_suspicious: bool = True