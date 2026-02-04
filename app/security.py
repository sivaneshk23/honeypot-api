import os
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict
from fastapi import HTTPException, Header, Request, status

class SecurityManager:
    """Security manager with static API key"""
    
    def __init__(self):
        # STATIC API KEY - Never changes
        self.api_keys = {
            "GUVI_HCL_2025_EVAL": {
                "key": os.getenv("EVAL_API_KEY", "GUVI_HCL_2025_EVAL_YGHn9UoBVBrhoru4q2nDYIMiIHacB9QT"),
                "created": datetime.utcnow().isoformat(),
                "expires": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "rate_limit": 1000,
                "active": True
            }
        }
        
        self.rate_limits = {}
    
    def validate_api_key(
        self,
        request: Request,
        x_api_key: Optional[str] = Header(None)
    ) -> Tuple[bool, str]:
        """Validate API key"""
        
        if not x_api_key:
            raise HTTPException(status_code=401, detail="API key is required")
        
        # Find matching key
        for name, info in self.api_keys.items():
            if info["key"] == x_api_key:
                if not info["active"]:
                    raise HTTPException(status_code=401, detail="API key deactivated")
                
                # Check expiration
                expires_at = datetime.fromisoformat(info["expires"].replace('Z', '+00:00'))
                if datetime.utcnow() > expires_at:
                    raise HTTPException(status_code=401, detail="API key expired")
                
                # Simple rate limiting
                client_ip = request.client.host or "unknown"
                rate_key = f"{name}:{client_ip}:{int(time.time() // 60)}"
                
                current_count = self.rate_limits.get(rate_key, 0)
                if current_count >= info["rate_limit"]:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                
                self.rate_limits[rate_key] = current_count + 1
                return True, name
        
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    def get_key_for_submission(self) -> str:
        """Get the evaluation API key for submission"""
        return self.api_keys["GUVI_HCL_2025_EVAL"]["key"]

# Global instance
security_manager = SecurityManager()

# FastAPI dependency
async def verify_api_key(
    request: Request,
    x_api_key: str = Header(..., description="Your API key")
):
    """Dependency for API key verification"""
    is_valid, key_type = security_manager.validate_api_key(request, x_api_key)
    return key_type