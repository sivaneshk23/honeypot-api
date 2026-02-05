"""
Security module for API key verification
"""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional

# GUVI evaluation API key
GUVI_API_KEY = "GUVI_HCL_2025_EVAL_YGHn9UoBVBrhoru4q2nDYIMiIHacB9QT"

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Verify API key for GUVI evaluation
    
    In production, this would check against a database
    For GUVI hackathon, we accept their evaluation key
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )
    
    # Accept GUVI evaluation key
    if api_key == GUVI_API_KEY:
        return "guvi_evaluation"
    
    # For testing, accept any key that starts with "test"
    if api_key.startswith("test_"):
        return "test_key"
    
    raise HTTPException(
        status_code=401,
        detail="Invalid API key"
    )