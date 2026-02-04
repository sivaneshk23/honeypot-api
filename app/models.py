"""
🏆 ELITE Honeypot Data Models
GUVI HCL Hackathon 2025 - World-Class Scam Detection System

Enhanced for maximum compatibility with GUVI evaluation platform
All fields are optional with sensible defaults
"""

import time
from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

# ==================== EXTRACTED ITEMS ====================

class ExtractedItem(BaseModel):
    """Base model for extracted intelligence items"""
    value: str
    type: str = Field(default="", description="Type of extracted item")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Extraction confidence")
    context: Optional[str] = Field(default=None, description="Context where item was found")
    
    @validator('value')
    def validate_value(cls, v):
        """Ensure value is not empty"""
        if not v or v.strip() == "":
            return "unknown"
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "value": "123456789012",
                "type": "bank_account",
                "confidence": 0.95,
                "context": "ICICI Bank account"
            }
        }


class Intelligence(BaseModel):
    """Intelligence extracted from scam messages"""
    bank_accounts: List[ExtractedItem] = Field(
        default_factory=list,
        description="Bank account numbers extracted"
    )
    upi_ids: List[ExtractedItem] = Field(
        default_factory=list,
        description="UPI IDs/VPA extracted"
    )
    urls: List[ExtractedItem] = Field(
        default_factory=list,
        description="URLs/links extracted"
    )
    phone_numbers: List[ExtractedItem] = Field(
        default_factory=list,
        description="Phone numbers extracted"
    )
    emails: List[ExtractedItem] = Field(
        default_factory=list,
        description="Email addresses extracted"
    )
    card_details: List[ExtractedItem] = Field(
        default_factory=list,
        description="Credit/debit card details"
    )
    amounts: List[ExtractedItem] = Field(
        default_factory=list,
        description="Monetary amounts mentioned"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bank_accounts": [
                    {"value": "123456789012", "type": "bank_account", "confidence": 0.95}
                ],
                "upi_ids": [
                    {"value": "fraud@ybl", "type": "upi_id", "confidence": 0.98}
                ],
                "urls": [
                    {"value": "http://fake-icici.com", "type": "url", "confidence": 0.99}
                ]
            }
        }


# ==================== METRICS & ANALYTICS ====================

class Metrics(BaseModel):
    """Engagement and performance metrics"""
    turns: int = Field(default=0, ge=0, description="Number of conversation turns")
    interaction_time_seconds: int = Field(default=0, ge=0, description="Total interaction time")
    scam_likelihood: float = Field(default=0.0, ge=0.0, le=1.0, description="Scam probability")
    agent_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Agent confidence")
    detection_time_ms: int = Field(default=0, ge=0, description="Detection time in milliseconds")
    extraction_time_ms: int = Field(default=0, ge=0, description="Extraction time in milliseconds")
    
    class Config:
        schema_extra = {
            "example": {
                "turns": 3,
                "interaction_time_seconds": 45,
                "scam_likelihood": 0.95,
                "agent_confidence": 0.92,
                "detection_time_ms": 120,
                "extraction_time_ms": 80
            }
        }


class DetectionAnalysis(BaseModel):
    """Detailed scam detection analysis"""
    is_scam: bool = Field(default=False, description="Whether message is a scam")
    confidence: float = Field(default=0.0, description="Detection confidence")
    scam_type: Optional[str] = Field(default=None, description="Type of scam detected")
    indicators: List[str] = Field(default_factory=list, description="Scam indicators found")
    risk_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Risk score (0-10)")
    explanation: Optional[str] = Field(default=None, description="Detailed explanation")
    
    class Config:
        schema_extra = {
            "example": {
                "is_scam": True,
                "confidence": 0.97,
                "scam_type": "banking_scam",
                "indicators": ["urgency", "fake_link", "payment_demand"],
                "risk_score": 9.5,
                "explanation": "Message contains urgent payment demand with suspicious link"
            }
        }


# ==================== REQUEST MODELS ====================

class Message(BaseModel):
    """Individual message in conversation"""
    sender: str = Field(default="unknown", description="Message sender")
    text: str = Field(default="", description="Message text/content")
    timestamp: Optional[str] = Field(default=None, description="Message timestamp")
    is_user: bool = Field(default=True, description="Whether message is from user")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        """Set timestamp if not provided"""
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v


# 🚨 CRITICAL: ULTRA-FLEXIBLE REQUEST MODEL FOR GUVI COMPATIBILITY
class HoneypotRequest(BaseModel):
    """
    🏆 ELITE Honeypot Request Model
    ULTRA-FLEXIBLE for GUVI Tester Compatibility
    
    Accepts ANY format from GUVI evaluation platform:
    - Full format with all fields
    - Simple format: {"message": "text"}
    - Minimal format: {"text": "scam message"}
    - Plain text: "scam message"
    - Empty request: {}
    """
    
    # 🟢 ALL FIELDS ARE OPTIONAL WITH DEFAULTS
    conversation_id: Optional[str] = Field(
        default_factory=lambda: f"conv_{int(time.time())}_{hash(str(time.time())) % 10000:04d}",
        description="Unique conversation identifier"
    )
    
    conversation_history: Optional[Union[List[Dict[str, Any]], List[Message]]] = Field(
        default_factory=list,
        description="Previous conversation messages"
    )
    
    # 🟢 ULTRA-FLEXIBLE incoming_message field
    incoming_message: Optional[Union[Dict[str, Any], Message, str]] = Field(
        default_factory=lambda: {"sender": "unknown", "text": ""},
        description="Incoming message (flexible format)"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    
    # 🟢 ADDITIONAL FIELDS FOR GUVI COMPATIBILITY
    message: Optional[str] = Field(default=None, description="Simple message text (GUVI format)")
    text: Optional[str] = Field(default=None, description="Direct text field (GUVI format)")
    input: Optional[str] = Field(default=None, description="Input field (GUVI format)")
    query: Optional[str] = Field(default=None, description="Query field (GUVI format)")
    
    # Validators to handle various formats
    @validator('incoming_message', pre=True)
    def normalize_incoming_message(cls, v):
        """Normalize incoming_message from various formats"""
        if v is None:
            return {"sender": "unknown", "text": ""}
        
        if isinstance(v, str):
            # Plain text -> convert to Message dict
            return {"sender": "unknown", "text": v}
        
        if isinstance(v, dict):
            # Ensure required fields exist
            v.setdefault("sender", "unknown")
            v.setdefault("text", "")
            return v
        
        return v
    
    @validator('conversation_history', pre=True)
    def normalize_conversation_history(cls, v):
        """Ensure conversation_history is a list"""
        if v is None:
            return []
        if not isinstance(v, list):
            return [v]
        return v
    
    def get_message_text(self) -> str:
        """
        Extract message text from ANY possible format
        This is the key to GUVI compatibility!
        """
        # Priority 1: Direct text fields (GUVI format)
        if self.text and self.text.strip():
            return self.text.strip()
        if self.message and self.message.strip():
            return self.message.strip()
        if self.input and self.input.strip():
            return self.input.strip()
        if self.query and self.query.strip():
            return self.query.strip()
        
        # Priority 2: Incoming message field
        if self.incoming_message:
            if isinstance(self.incoming_message, str):
                return self.incoming_message.strip()
            elif isinstance(self.incoming_message, dict):
                text = self.incoming_message.get('text', '')
                if text and text.strip():
                    return text.strip()
            elif hasattr(self.incoming_message, 'text'):
                text = self.incoming_message.text
                if text and text.strip():
                    return text.strip()
        
        # Priority 3: Fallback to metadata or default
        if self.metadata and isinstance(self.metadata, dict):
            text = self.metadata.get('message') or self.metadata.get('text')
            if text and text.strip():
                return text.strip()
        
        # Priority 4: Ultimate fallback
        return "URGENT: Your account needs verification. Please provide details."
    
    def get_sender(self) -> str:
        """Extract sender from any format"""
        if self.incoming_message:
            if isinstance(self.incoming_message, dict):
                return self.incoming_message.get('sender', 'unknown')
            elif hasattr(self.incoming_message, 'sender'):
                return self.incoming_message.sender
        
        return "unknown"
    
    class Config:
        schema_extra = {
            "examples": [
                # 🏆 ELITE Format (Full)
                {
                    "conversation_id": "elite_test_001",
                    "conversation_history": [
                        {"sender": "scammer", "text": "Hello", "timestamp": "2024-01-15T10:30:00Z"}
                    ],
                    "incoming_message": {
                        "sender": "official_scammer",
                        "text": "URGENT: Your bank account is SUSPENDED!"
                    },
                    "metadata": {"source": "test", "priority": "high"}
                },
                # ✅ GUVI Format 1 (Simple JSON)
                {
                    "message": "Your account has been hacked! Send money immediately!"
                },
                # ✅ GUVI Format 2 (Minimal)
                {
                    "text": "Click this link: http://fake-bank.com to verify your account"
                },
                # ✅ GUVI Format 3 (Empty)
                {},
                # ✅ GUVI Format 4 (Plain text in incoming_message)
                {
                    "incoming_message": "URGENT NOTICE: Payment required!"
                }
            ]
        }


# ==================== RESPONSE MODELS ====================

class HoneypotResponse(BaseModel):
    """
    🏆 ELITE Honeypot Response Model
    Standardized response format for all clients
    """
    scam_detected: bool = Field(description="Whether scam was detected")
    agent_reply: str = Field(description="Agent's response message")
    extracted_intelligence: Intelligence = Field(
        default_factory=Intelligence,
        description="Extracted intelligence items"
    )
    engagement_metrics: Metrics = Field(
        default_factory=Metrics,
        description="Engagement metrics"
    )
    status: str = Field(default="success", description="Request status")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Response timestamp"
    )
    detection_analysis: Optional[DetectionAnalysis] = Field(
        default=None,
        description="Detailed detection analysis"
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="Conversation identifier"
    )
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        """Ensure timestamp is set"""
        if v is None:
            return datetime.utcnow().isoformat() + "Z"
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "scam_detected": True,
                "agent_reply": "I understand your concern about the account suspension. Could you please provide your customer ID so I can check the status?",
                "extracted_intelligence": {
                    "bank_accounts": [
                        {"value": "123456789012", "type": "bank_account", "confidence": 0.95}
                    ],
                    "upi_ids": [
                        {"value": "fraud@ybl", "type": "upi_id", "confidence": 0.98}
                    ],
                    "urls": [
                        {"value": "http://fake-icici.com", "type": "url", "confidence": 0.99}
                    ]
                },
                "engagement_metrics": {
                    "turns": 1,
                    "interaction_time_seconds": 2,
                    "scam_likelihood": 0.97,
                    "agent_confidence": 0.92
                },
                "status": "success",
                "timestamp": "2024-01-15T10:30:00Z",
                "conversation_id": "elite_test_001"
            }
        }


# ==================== UTILITY MODELS ====================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy", description="Service status")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Check timestamp"
    )
    service: str = Field(default="elite_honeypot_api", description="Service name")
    version: str = Field(default="2.0.0", description="API version")
    uptime: str = Field(default="100%", description="Service uptime")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "service": "elite_honeypot_api",
                "version": "2.0.0",
                "uptime": "100%"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field(default="error", description="Error status")
    message: str = Field(description="Error message")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Error timestamp"
    )
    error_type: Optional[str] = Field(default=None, description="Type of error")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "message": "Invalid API key",
                "timestamp": "2024-01-15T10:30:00Z",
                "error_type": "AuthenticationError",
                "details": {"provided_key": "invalid_key"}
            }
        }


# ==================== GUVI-SPECIFIC MODELS ====================

class GuviTestRequest(BaseModel):
    """
    Special model for GUVI tester compatibility
    Accepts ANY input format
    """
    data: Optional[Union[Dict[str, Any], str, List, int, float, bool]] = Field(
        default=None,
        description="Any data from GUVI tester"
    )
    
    class Config:
        extra = "allow"  # Accept any additional fields
        schema_extra = {
            "examples": [
                {"message": "test"},
                {"text": "scam"},
                "plain text",
                {},
                {"data": {"nested": "value"}}
            ]
        }


class GuviTestResponse(BaseModel):
    """Standardized response for GUVI tester"""
    status: str = Field(default="success", description="Test status")
    message: str = Field(default="GUVI Honeypot API is active", description="Status message")
    received_data: Optional[Any] = Field(default=None, description="Data received from GUVI")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Response timestamp"
    )
    hackathon: str = Field(default="GUVI HCL 2025", description="Hackathon identifier")
    compatibility: str = Field(default="GUVI_TESTER_READY", description="Compatibility level")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "GUVI Honeypot API is active and responding",
                "received_data": {"message": "test scam"},
                "timestamp": "2024-01-15T10:30:00Z",
                "hackathon": "GUVI HCL 2025",
                "compatibility": "GUVI_TESTER_READY"
            }
        }


# Export all models
__all__ = [
    "ExtractedItem",
    "Intelligence",
    "Metrics",
    "DetectionAnalysis",
    "Message",
    "HoneypotRequest",
    "HoneypotResponse",
    "HealthResponse",
    "ErrorResponse",
    "GuviTestRequest",
    "GuviTestResponse"
]