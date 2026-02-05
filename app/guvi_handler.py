"""
🏆 ELITE GUVI HANDLER
Handles GUVI format exactly and ensures perfect compatibility
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import requests
from app.models import (
    GuviRequest, GuviResponse, FinalResult, 
    Message, ConversationState, Intelligence, ExtractedItem
)
from app.detector.classifier import scam_detector
from app.agent.orchestrator import agent_orchestrator
from app.extractor.patterns import intelligence_extractor
from app.memory import conversation_memory


class EliteGuviHandler:
    """
    🏆 ELITE HANDLER FOR GUVI HACKATHON
    Processes GUVI format and returns EXACT expected response
    """
    
    # Store active conversations
    conversations: Dict[str, ConversationState] = {}
    
    @staticmethod
    def generate_session_hash(session_id: str) -> str:
        """Generate hash for session tracking"""
        return hashlib.md5(session_id.encode()).hexdigest()[:8]
    
    def process_guvi_request(self, request: GuviRequest) -> GuviResponse:
        """
        🎯 MAIN PROCESSING FUNCTION
        Takes GUVI format, processes through elite system, returns GUVI format
        """
        session_id = request.sessionId
        
        print(f"\n🎯 PROCESSING GUVI REQUEST FOR SESSION: {session_id}")
        print(f"📨 Message: {request.message.text[:100]}...")
        print(f"📊 History: {len(request.conversationHistory)} previous messages")
        
        # Get or create conversation state
        if session_id not in self.conversations:
            self.conversations[session_id] = ConversationState(
                session_id=session_id,
                messages=[],
                scam_detected=False,
                scam_confidence=0.0
            )
            print(f"🆕 New conversation started: {session_id}")
        
        state = self.conversations[session_id]
        
        # Update message history
        all_messages = state.messages + request.conversationHistory + [request.message]
        state.messages = all_messages
        
        # 🔥 ELITE SCAM DETECTION
        scam_detected, scam_confidence, detection_analysis = scam_detector.detect_scam(
            request.message.text
        )
        
        # Update scam detection state
        if scam_confidence > 0.7 and not state.scam_detected:
            state.scam_detected = True
            state.scam_confidence = scam_confidence
            print(f"🚨 SCAM DETECTED! Confidence: {scam_confidence:.1%}")
        
        # 🔍 ELITE INTELLIGENCE EXTRACTION
        extracted_raw = intelligence_extractor.extract_all(request.message.text)
        
        # Update intelligence in state
        for item_type, items in extracted_raw.items():
            if items:
                for item in items:
                    if isinstance(item, dict):
                        elite_item = ExtractedItem(
                            value=item.get('value', ''),
                            type=item.get('type', item_type),
                            confidence=item.get('confidence', 0.8)
                        )
                        
                        # Add to appropriate list
                        if item_type == "bank_accounts":
                            state.extracted_intelligence.bank_accounts.append(elite_item)
                        elif item_type == "upi_ids":
                            state.extracted_intelligence.upi_ids.append(elite_item)
                        elif item_type == "urls":
                            state.extracted_intelligence.urls.append(elite_item)
                        elif item_type == "phone_numbers":
                            state.extracted_intelligence.phone_numbers.append(elite_item)
                        elif item_type == "emails":
                            state.extracted_intelligence.emails.append(elite_item)
        
        # 🤖 ELITE AGENT RESPONSE GENERATION
        agent_reply = ""
        
        if state.scam_detected:
            # Use elite agent for scam engagement
            agent_reply = agent_orchestrator.generate_response(
                turns=len(state.messages),
                scam_confidence=state.scam_confidence,
                extracted_intelligence=extracted_raw,
                context={
                    "session_id": session_id,
                    "persona": state.agent_persona,
                    "engagement_level": state.engagement_level
                }
            )
            
            # Increase engagement level
            state.engagement_level += 1
            
            # Check if engagement is complete (send final callback)
            if state.engagement_level >= 8:  # After sufficient engagement
                self._send_final_callback(state)
                
        else:
            # For non-scams or initial messages
            agent_reply = self._generate_initial_response(request.message.text, scam_confidence)
        
        # Prepare GUVI-compatible response
        response = GuviResponse(
            status="success",
            reply=agent_reply
        )
        
        print(f"✅ Response generated: {agent_reply[:80]}...")
        print(f"📊 State: Scam={state.scam_detected}, Confidence={state.scam_confidence:.1%}")
        print(f"📈 Engagement Level: {state.engagement_level}")
        
        return response
    
    def _generate_initial_response(self, message: str, scam_confidence: float) -> str:
        """Generate initial response based on scam confidence"""
        
        responses = {
            "high_scam": [
                "Why is my account being suspended? I didn't receive any official notification.",
                "This is concerning. Which bank are you referring to exactly?",
                "I need to verify this. What's your employee ID and department?",
                "Can you provide the official reference number for this notice?"
            ],
            "medium_scam": [
                "I'm not sure I understand. Can you explain what needs verification?",
                "Which account are you referring to? I have multiple accounts.",
                "I'll need more details before proceeding with any verification.",
                "Can you send this through official bank channels instead?"
            ],
            "low_scam": [
                "Thank you for the message. I'll check with my bank directly.",
                "I'll verify this through my banking app. Thank you.",
                "Please provide more details through official communication.",
                "I need to confirm this with customer service first."
            ]
        }
        
        import random
        
        if scam_confidence > 0.7:
            return random.choice(responses["high_scam"])
        elif scam_confidence > 0.4:
            return random.choice(responses["medium_scam"])
        else:
            return random.choice(responses["low_scam"])
    
    def _send_final_callback(self, state: ConversationState):
        """
        🎯 MANDATORY: Send final callback to GUVI evaluation endpoint
        This is CRITICAL for scoring
        """
        try:
            # Convert elite intelligence to GUVI format
            intelligence_dict = {
                "bankAccounts": [item.value for item in state.extracted_intelligence.bank_accounts],
                "upiIds": [item.value for item in state.extracted_intelligence.upi_ids],
                "phishingLinks": [item.value for item in state.extracted_intelligence.urls],
                "phoneNumbers": [item.value for item in state.extracted_intelligence.phone_numbers],
                "suspiciousKeywords": self._extract_keywords(state.messages)
            }
            
            # Prepare final result
            final_result = FinalResult(
                sessionId=state.session_id,
                scamDetected=state.scam_detected,
                totalMessagesExchanged=len(state.messages),
                extractedIntelligence=intelligence_dict,
                agentNotes=f"Scammer used urgency tactics. Engagement level: {state.engagement_level}. "
                          f"Scam confidence: {state.scam_confidence:.1%}. "
                          f"Extracted {len(intelligence_dict['bankAccounts'])} bank accounts, "
                          f"{len(intelligence_dict['upiIds'])} UPI IDs."
            )
            
            # Send to GUVI endpoint
            callback_url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
            
            response = requests.post(
                callback_url,
                json=final_result.dict(),
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ FINAL CALLBACK SENT SUCCESSFULLY for session: {state.session_id}")
                print(f"📤 Sent to: {callback_url}")
                print(f"📊 Response: {response.status_code}")
                
                # Clear conversation after successful callback
                if state.session_id in self.conversations:
                    del self.conversations[state.session_id]
            else:
                print(f"⚠️ Callback failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending final callback: {e}")
    
    def _extract_keywords(self, messages: List[Message]) -> List[str]:
        """Extract suspicious keywords from conversation"""
        suspicious_keywords = [
            "urgent", "immediate", "suspend", "block", "verify", 
            "payment", "upi", "account", "bank", "click", "link",
            "secure", "confirm", "final", "warning", "danger",
            "threat", "action required", "immediately", "now"
        ]
        
        found_keywords = set()
        for msg in messages:
            text_lower = msg.text.lower()
            for keyword in suspicious_keywords:
                if keyword in text_lower:
                    found_keywords.add(keyword)
        
        return list(found_keywords)
    
    def get_conversation_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a conversation"""
        if session_id in self.conversations:
            state = self.conversations[session_id]
            return {
                "session_id": session_id,
                "total_messages": len(state.messages),
                "scam_detected": state.scam_detected,
                "scam_confidence": state.scam_confidence,
                "engagement_level": state.engagement_level,
                "extracted_items": {
                    "bank_accounts": len(state.extracted_intelligence.bank_accounts),
                    "upi_ids": len(state.extracted_intelligence.upi_ids),
                    "urls": len(state.extracted_intelligence.urls),
                    "phone_numbers": len(state.extracted_intelligence.phone_numbers)
                }
            }
        return None


# Create singleton instance
guvi_handler = EliteGuviHandler()