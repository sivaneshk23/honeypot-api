import random
import time
from typing import Dict

class EliteAgentOrchestrator:
    """Elite Honeypot Agent - Masters Social Engineering"""
    
    def __init__(self):
        # Multi-stage response strategies
        self.response_strategies = {
            "initial_engagement": {
                "stage": 0,
                "responses": [
                    "Hi, I received your message.",
                    "Hello, who is this?",
                    "I got a notification about this.",
                    "Is this regarding the recent message I received?",
                    "Can you tell me more about this?",
                    "I'm not sure I understand, can you explain?",
                    "This is concerning. What should I do?"
                ]
            },
            "playing_dumb": {
                "stage": 1,
                "responses": [
                    "I'm not very tech-savvy. Can you guide me through this?",
                    "My app keeps showing errors. What do I do?",
                    "I tried but it's not working. Can you help step by step?",
                    "Sorry, I'm new to this. Can you explain like I'm a beginner?",
                    "Which option should I select? I'm confused.",
                    "The website is loading slowly. Is that normal?",
                    "My phone is old. Will that cause any issues?"
                ]
            },
            "seeking_assurance": {
                "stage": 2,
                "responses": [
                    "Are you sure this is safe? I've heard about scams.",
                    "Can you provide official verification?",
                    "Is there a customer care number I can call to confirm?",
                    "This seems urgent. Why wasn't I notified earlier?",
                    "Can you send this in writing or email?",
                    "I need to check with my family first.",
                    "What happens if I don't do this immediately?"
                ]
            },
            "extraction_phase": {
                "stage": 3,
                "responses": [
                    "What details exactly do you need from me?",
                    "Can you share your UPI ID again? I didn't save it.",
                    "What's the account number where I should send money?",
                    "Can you send the link one more time?",
                    "Should I share my bank details here or somewhere else?",
                    "Is it okay to share my Aadhaar number for verification?",
                    "What's the website where I need to enter my details?"
                ]
            },
            "delaying_tactics": {
                "stage": 4,
                "responses": [
                    "My internet is slow. Please wait.",
                    "Let me charge my phone first.",
                    "I need to find my debit card. One minute.",
                    "The OTP hasn't arrived yet. Should I request again?",
                    "My bank app needs an update. It's taking time.",
                    "I'm at work. Can we continue in 10 minutes?",
                    "Let me check with my bank once."
                ]
            }
        }
        
        # Context-aware response modifiers
        self.modifiers = {
            "concerned": ["Actually, ", "Wait, ", "Hmm... ", "Sorry, "],
            "urgent": ["Quickly, ", "Immediately, ", "Asap, ", "Right now, "],
            "confused": ["I think ", "Maybe ", "Probably ", "Perhaps "],
            "agreeable": ["Okay, ", "Alright, ", "Sure, ", "Yes, "]
        }
        
        # Filler phrases for natural conversation
        self.fillers = [
            "please", "sorry", "brother", "sir", "madam",
            "actually", "basically", "like", "you know"
        ]
    
    def analyze_context(self, turn_count: int, scam_confidence: float, extracted_items: Dict) -> Dict:
        """Analyze conversation context for optimal response"""
        context = {
            "stage": min(turn_count // 2, 4),  # Progress through stages
            "urgency_level": "high" if scam_confidence > 0.7 else "medium",
            "has_financial_info": any(len(items) > 0 for key, items in extracted_items.items() 
                                     if key in ['bank_accounts', 'upi_ids', 'card_details']),
            "needs_more_info": turn_count < 3 or not any(len(items) > 0 for items in extracted_items.values())
        }
        
        # Adjust stage based on extracted intelligence
        if context["has_financial_info"] and turn_count > 1:
            context["stage"] = min(context["stage"] + 1, 4)
        
        return context
    
    def select_strategy(self, context: Dict) -> str:
        """Select response strategy based on context"""
        if context["stage"] == 0:
            return "initial_engagement"
        elif context["stage"] == 1:
            return "playing_dumb"
        elif context["stage"] == 2:
            if context["urgency_level"] == "high":
                return "seeking_assurance"
            else:
                return "playing_dumb"
        elif context["stage"] == 3:
            if context["has_financial_info"]:
                return "extraction_phase"
            else:
                return "seeking_assurance"
        else:
            return "delaying_tactics"
    
    def generate_response(self, turn_count: int, scam_confidence: float, 
                         extracted_intelligence: Dict = None) -> str:
        """Generate elite agent response"""
        if extracted_intelligence is None:
            extracted_intelligence = {}
        
        # Analyze context
        context = self.analyze_context(turn_count, scam_confidence, extracted_intelligence)
        
        # Select strategy
        strategy = self.select_strategy(context)
        strategy_data = self.response_strategies[strategy]
        
        # Base response
        base_response = random.choice(strategy_data["responses"])
        
        # Add modifier based on context
        if context["urgency_level"] == "high":
            modifier = random.choice(self.modifiers["concerned"])
        elif turn_count < 2:
            modifier = random.choice(self.modifiers["confused"])
        else:
            modifier = random.choice(self.modifiers["agreeable"])
        
        response = modifier + base_response
        
        # Add filler for naturalness (30% chance)
        if random.random() < 0.3:
            filler = random.choice(self.fillers)
            response = response + " " + filler
        
        # Add specific extraction prompts if in extraction phase
        if strategy == "extraction_phase":
            missing_items = []
            if not extracted_intelligence.get("bank_accounts"):
                missing_items.append("bank account number")
            if not extracted_intelligence.get("upi_ids"):
                missing_items.append("UPI ID")
            if not extracted_intelligence.get("urls"):
                missing_items.append("website link")
            
            if missing_items and random.random() < 0.5:
                item = random.choice(missing_items)
                response = response + " What's the " + item + "?"
        
        # Add urgency if scam confidence is high
        if scam_confidence > 0.8 and random.random() < 0.4:
            urgency_phrases = ["It's very urgent!", "Please hurry!", "Time is running out!"]
            response = response + " " + random.choice(urgency_phrases)
        
        # Ensure response length
        response = response[:497] + "..." if len(response) > 500 else response
        
        print(f"🤖 AGENT RESPONSE GENERATED:")
        print(f"   Stage: {context['stage']}, Strategy: {strategy}")
        print(f"   Response: '{response}'")
        
        return response

# Global instance
agent_orchestrator = EliteAgentOrchestrator()