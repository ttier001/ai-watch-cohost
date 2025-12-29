"""User trust and behavior analysis service"""
import json
from anthropic import Anthropic
from app.config import settings
from app.models.schemas import UserBehaviorInput, TrustAnalysis, SellerModerationSettings


class UserAnalysisService:
    """Service for analyzing user behavior and trust"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL

    def analyze_user(self, user_data: UserBehaviorInput) -> TrustAnalysis:
        """Analyze user behavior and assign trust score"""
        
        prompt = f"""Analyze this live stream chat user and assess their trustworthiness.
USER PROFILE:

Username: {user_data.username}
Current Message: "{user_data.message}"
Recent Message History: {json.dumps(user_data.message_history) if user_data.message_history else "No history"}
Account Age: {user_data.account_age_days} days
Previous Purchases: {user_data.previous_purchases}
Platform Verified: {user_data.is_verified}
Followers: {user_data.follower_count or 'Unknown'}

ANALYSIS CRITERIA:
BOT INDICATORS:

Repetitive messages, spam phrases
Generic "Check out my..." messages
Excessive emojis/special characters
Rapid identical messages
Random username patterns
No genuine product engagement

TROLL INDICATORS:

Inflammatory language
Time-wasting questions
Attempts to derail conversation
Baiting/provocative statements
Personal attacks

SCAMMER INDICATORS:

Off-platform communication requests
Suspicious payment mentions
Phishing attempts
Too-good-to-be-true offers

GENUINE BUYER INDICATORS:

Specific product questions
Legitimate purchasing interest
Respectful tone
Previous purchase history
Verified account

Respond with ONLY valid JSON:
{{
"trust_score": 0-100,
"classification": "verified_buyer|casual_viewer|suspicious|likely_bot|troll|scammer",
"risk_level": "low|medium|high|critical",
"flags": ["specific concerns"],
"reasoning": "brief explanation",
"recommended_action": "allow|review|warn|restrict|block"
}}

SCORING:

80-100: Verified buyer, established, genuine
60-79: Casual viewer, legitimate
40-59: Suspicious, monitor
20-39: Likely bot/troll, restrict
0-19: Clear bot/scammer, block
"""

        try:
            message_obj = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(message_obj.content[0].text)
            
            return TrustAnalysis(
                username=user_data.username,
                trust_score=result["trust_score"],
                classification=result["classification"],
                risk_level=result["risk_level"],
                flags=result.get("flags", []),
                reasoning=result["reasoning"],
                recommended_action=result["recommended_action"]
            )
            
        except json.JSONDecodeError as e:
            return TrustAnalysis(
                username=user_data.username,
                trust_score=50.0,
                classification="suspicious",
                risk_level="medium",
                flags=["Analysis error - manual review"],
                reasoning=f"Error: {str(e)}",
                recommended_action="review"
            )
        except Exception as e:
            raise Exception(f"User analysis error: {str(e)}")

    def should_allow_interaction(
        self,
        trust_analysis: TrustAnalysis,
        moderation_settings: SellerModerationSettings
    ) -> tuple[bool, str]:
        """Determine if user should be allowed to interact"""
        if trust_analysis.risk_level == "critical":
            return False, f"User blocked: {trust_analysis.classification}"
        
        if moderation_settings.auto_block_bots and trust_analysis.classification == "likely_bot":
            return False, "Automated bot detected"
        
        if moderation_settings.auto_block_trolls and trust_analysis.classification == "troll":
            return False, "Disruptive behavior detected"
        
        if trust_analysis.trust_score < moderation_settings.min_trust_score:
            return False, f"Trust score too low ({trust_analysis.trust_score}/{moderation_settings.min_trust_score})"
        
        if moderation_settings.require_verification and trust_analysis.classification not in ["verified_buyer"]:
            return False, "Verified buyers only"
        
        if trust_analysis.risk_level == "high":
            return True, f"⚠️ Warning: {', '.join(trust_analysis.flags)}"
        
        return True, "User cleared"
