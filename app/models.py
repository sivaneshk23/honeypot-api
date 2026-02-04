from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(..., description="Sender identifier")
    text: str = Field(..., description="Message content")
    
    @validator('sender', 'text')
    def check_not_empty(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return "unknown"
        return v

class HoneypotRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation ID")
    conversation_history: List[Union[Message, Dict[str, Any]]] = Field(default_factory=list)
    incoming_message: Union[Message, Dict[str, Any]] = Field(..., description="New incoming message")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('incoming_message')
    def validate_incoming_message(cls, v):
        if isinstance(v, dict):
            # Ensure required fields exist
            if 'sender' not in v:
                v['sender'] = 'unknown'
            if 'text' not in v:
                v['text'] = ''
            return Message(**v)
        return v
    
    @validator('conversation_history')
    def validate_conversation_history(cls, v):
        validated = []
        for item in v:
            if isinstance(item, dict):
                if 'sender' not in item:
                    item['sender'] = 'unknown'
                if 'text' not in item:
                    item['text'] = ''
                validated.append(Message(**item))
            else:
                validated.append(item)
        return validated

class ExtractedItem(BaseModel):
    value: str = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    @validator('confidence')
    def validate_confidence(cls, v):
        return float(v)

class Intelligence(BaseModel):
    bank_accounts: List[ExtractedItem] = Field(default_factory=list)
    upi_ids: List[ExtractedItem] = Field(default_factory=list)
    urls: List[ExtractedItem] = Field(default_factory=list)

class Metrics(BaseModel):
    turns: int = Field(..., ge=0)
    interaction_time_seconds: int = Field(..., ge=0)
    scam_likelihood: float = Field(..., ge=0.0, le=1.0)
    agent_confidence: float = Field(..., ge=0.0, le=1.0)
    
    @validator('turns', 'interaction_time_seconds')
    def validate_ints(cls, v):
        return int(v) if v else 0
    
    @validator('scam_likelihood', 'agent_confidence')
    def validate_floats(cls, v):
        return float(v) if v else 0.0

class HoneypotResponse(BaseModel):
    scam_detected: bool = Field(..., description="Whether scam is detected")
    agent_reply: str = Field(..., description="Agent's response message")
    extracted_intelligence: Intelligence = Field(..., description="Extracted scam intelligence")
    engagement_metrics: Metrics = Field(..., description="Engagement metrics")
    status: str = Field("success", description="Response status")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    @validator('agent_reply')
    def validate_agent_reply(cls, v):
        return str(v) if v else ""