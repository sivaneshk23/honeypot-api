from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import time
from datetime import datetime

# Import models and components
from app.models import HoneypotRequest, HoneypotResponse, Intelligence, Metrics, ExtractedItem
from app.security import verify_api_key
from app.detector.classifier import scam_classifier
from app.agent.orchestrator import agent_orchestrator
from app.extractor.patterns import intelligence_extractor
from app.memory import conversation_memory
from app.utils.logger import setup_logger

# Setup logger
logger = setup_logger("honeypot_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info("🚀 Starting Agentic Honeypot API")
    logger.info(f"📊 API Key: GUVI_HCL_2025_EVAL_YGHn9UoBVBrhoru4q2nDYIMiIHacB9QT")
    yield
    logger.info("🛑 Shutting down")

# Create FastAPI app
app = FastAPI(
    title="Agentic Honeypot API",
    description="AI-powered scam detection for GUVI HCL Hackathon",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "service": "Agentic Honeypot API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoint": "/honeypot",
        "authentication": "x-api-key header"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "honeypot_api",
        "uptime": "100%"
    }

@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot_endpoint(
    request: HoneypotRequest,
    background_tasks: BackgroundTasks,
    key_type: str = Depends(verify_api_key)
):
    """Main honeypot endpoint"""
    
    start_time = time.time()
    
    try:
        # Get conversation context
        context = conversation_memory.get_conversation(request.conversation_id)
        
        # Update turn count
        conversation_memory.update_turns(request.conversation_id)
        
        # Detect scam
        scam_detected, scam_confidence = scam_classifier.detect_scam(
            request.incoming_message.text
        )
        
        # Generate agent response if scam detected
        agent_reply = ""
        if scam_detected:
            agent_reply = agent_orchestrator.generate_response(
                context["turns"], scam_confidence
            )
        
        # Extract intelligence if scam detected
        extracted_raw = {}
        if scam_detected:
            extracted_raw = intelligence_extractor.extract_all(
                request.incoming_message.text
            )
        
        # Prepare response
        response = HoneypotResponse(
            scam_detected=scam_detected,
            agent_reply=agent_reply,
            extracted_intelligence=Intelligence(
                bank_accounts=[
                    ExtractedItem(**item) for item in extracted_raw.get("bank_accounts", [])
                ],
                upi_ids=[
                    ExtractedItem(**item) for item in extracted_raw.get("upi_ids", [])
                ],
                urls=[
                    ExtractedItem(**item) for item in extracted_raw.get("urls", [])
                ]
            ),
            engagement_metrics=Metrics(
                turns=context["turns"],
                interaction_time_seconds=int(time.time() - context["start_time"]),
                scam_likelihood=scam_confidence,
                agent_confidence=0.9 if scam_detected else 0.0
            ),
            status="success",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        logger.info(f"✅ Processed {request.conversation_id}: scam={scam_detected}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        # Return error response (still valid schema)
        return HoneypotResponse(
            scam_detected=False,
            agent_reply="",
            extracted_intelligence=Intelligence(
                bank_accounts=[],
                upi_ids=[],
                urls=[]
            ),
            engagement_metrics=Metrics(
                turns=0,
                interaction_time_seconds=0,
                scam_likelihood=0.0,
                agent_confidence=0.0
            ),
            status="error",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )