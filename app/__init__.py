"""
🏆 ELITE AGENTIC HONEYPOT API

World-class scam detection and engagement system for GUVI HCL Hackathon 2025.

Modules:
- detector: Advanced scam detection algorithms
- agent: Intelligent conversation agent  
- extractor: Sophisticated intelligence extraction
- models: Data structures and validation
- security: API authentication and protection
- memory: Conversation tracking
- utils: Helper functions
"""

__version__ = "2.0.0"
__author__ = "GUVI HCL Hackathon Team"
__description__ = "World-Class AI-powered scam detection system"

# Export main components
from app.main import app
from app.models import HoneypotRequest, HoneypotResponse
from app.security import security_manager, verify_api_key