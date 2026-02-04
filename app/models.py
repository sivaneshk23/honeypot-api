from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(..., description="Sender identifier")
    text: str = Field(..., description="Message content")

class HoneypotRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation ID")
    conversation_history: List[Message] = Field(default_factory=list)
    incoming_message: Message = Field(..., description="New incoming message")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExtractedItem(BaseModel):
    value: str = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0.0, le=1.0)

class Intelligence(BaseModel):
    bank_accounts: List[ExtractedItem] = Field(default_factory=list)
    upi_ids: List[ExtractedItem] = Field(default_factory=list)
    urls: List[ExtractedItem] = Field(default_factory=list)

class Metrics(BaseModel):
    turns: int = Field(..., ge=0)
    interaction_time_seconds: int = Field(..., ge=0)
    scam_likelihood: float = Field(..., ge=0.0, le=1.0)
    agent_confidence: float = Field(..., ge=0.0, le=1.0)

class HoneypotResponse(BaseModel):
    scam_detected: bool = Field(..., description="Whether scam is detected")
    agent_reply: str = Field(..., description="Agent's response message")
    extracted_intelligence: Intelligence = Field(..., description="Extracted scam intelligence")
    engagement_metrics: Metrics = Field(..., description="Engagement metrics")
    status: str = Field("success", description="Response status")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")