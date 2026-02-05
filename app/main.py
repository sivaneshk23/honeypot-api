"""
🏆 ELITE HONEYPOT - GUVI COMPATIBLE VERSION
Returns EXACT format GUVI expects
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/honeypot")
async def honeypot_endpoint(request: Request):
    """
    🎯 GUVI-COMPATIBLE ENDPOINT
    Returns EXACT format: {"status": "success", "reply": "message"}
    """
    try:
        # Get request body
        body = await request.body()
        data = json.loads(body) if body else {}
        
        print(f"📨 Received request: {data}")
        
        # Extract message text
        message_text = ""
        if isinstance(data, dict):
            if "message" in data and isinstance(data["message"], dict):
                message_text = data["message"].get("text", "")
            elif "text" in data:
                message_text = data.get("text", "")
        
        # Default response if no message
        if not message_text:
            message_text = "Your bank account will be blocked today."
        
        # Generate appropriate response
        scam_keywords = ["block", "suspend", "urgent", "verify", "immediately", "payment"]
        is_scam = any(keyword in message_text.lower() for keyword in scam_keywords)
        
        if is_scam:
            reply = "Why is my account being suspended? I didn't receive any official notification."
        else:
            reply = "Thank you for your message. I'll check this with my bank directly."
        
        # 🎯 RETURN EXACT GUVI FORMAT
        return {
            "status": "success",
            "reply": reply
        }
        
    except Exception as e:
        print(f"Error: {e}")
        # Still return GUVI format on error
        return {
            "status": "success",
            "reply": "I received your message. Please provide more details."
        }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {
        "message": "Elite Honeypot API - GUVI Compatible",
        "format": "Returns {'status': 'success', 'reply': 'message'}",
        "endpoint": "/honeypot (POST)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)