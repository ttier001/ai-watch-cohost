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
