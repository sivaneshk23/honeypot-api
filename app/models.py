"""
🏆 ELITE HONEYPOT MODELS - GUVI COMPATIBLE
Updated to match GUVI evaluation format EXACTLY
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import time


# ==================== GUVI INPUT MODELS ====================

class Message(BaseModel):
    """Message model matching GUVI format exactly"""
    sender: str  # "scammer" or "user"
    text: str
    timestamp: int  # Epoch time in ms


class GuviRequest(BaseModel):
    """
    🎯 EXACT GUVI REQUEST FORMAT
    Matches the sample from GUVI documentation
    """
    sessionId: str = Field(..., alias="sessionId")
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    })
    
    class Config:
        allow_population_by_field_name = True


# ==================== GUVI OUTPUT MODELS ====================

class GuviResponse(BaseModel):
    """
    🎯 EXACT GUVI RESPONSE FORMAT
    Must return EXACTLY this format
    """
    status: str  # "success"
    reply: str   # Agent's response message


class FinalResult(BaseModel):
    """
    🎯 MANDATORY FINAL CALLBACK FORMAT
    Send this to GUVI after engagement
    """
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: Dict[str, List[str]]
    agentNotes: str


# ==================== ELITE INTELLIGENCE MODELS ====================

class ExtractedItem(BaseModel):
    """Intelligence item"""
    value: str
    type: str
    confidence: float


class Intelligence(BaseModel):
    """Elite intelligence extraction"""
    bank_accounts: List[ExtractedItem] = []
    upi_ids: List[ExtractedItem] = []
    urls: List[ExtractedItem] = []
    phone_numbers: List[ExtractedItem] = []
    emails: List[ExtractedItem] = []
    card_details: List[ExtractedItem] = []


class HoneypotMetrics(BaseModel):
    """Engagement metrics"""
    turns: int = 0
    scam_confidence: float = 0.0
    agent_confidence: float = 0.0


# ==================== CONVERSATION STATE ====================

class ConversationState(BaseModel):
    """Track conversation state"""
    session_id: str
    messages: List[Message] = []
    scam_detected: bool = False
    scam_confidence: float = 0.0
    extracted_intelligence: Intelligence = Field(default_factory=Intelligence)
    agent_persona: str = "concerned_customer"
    engagement_level: int = 1
    
    class Config:
        arbitrary_types_allowed = True


# Export all models
__all__ = [
    "Message",
    "GuviRequest",
    "GuviResponse",
    "FinalResult",
    "ExtractedItem",
    "Intelligence",
    "HoneypotMetrics",
    "ConversationState"
]