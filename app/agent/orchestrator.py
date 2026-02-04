import random

class AgentOrchestrator:
    """Generate agent responses"""
    
    def __init__(self):
        self.responses = {
            "initial": [
                "Hi, I got your message.",
                "Hello, who is this?",
                "I received this notification."
            ],
            "engagement": [
                "I'm not sure how to proceed.",
                "Can you explain again?",
                "My app is showing an error."
            ],
            "extraction": [
                "What bank details should I send?",
                "Please share your UPI ID.",
                "Can you send the link again?"
            ]
        }
    
    def generate_response(self, turn_count: int, scam_confidence: float) -> str:
        """Generate appropriate response"""
        if turn_count == 0:
            stage = "initial"
        elif turn_count < 3:
            stage = "engagement"
        else:
            stage = "extraction"
        
        base_response = random.choice(self.responses[stage])
        
        # Add natural variations
        variations = ["", "Hmm... ", "Actually, ", "Wait... "]
        response = random.choice(variations) + base_response
        
        # Add filler words occasionally
        if random.random() > 0.7:
            fillers = ["please", "sorry", "one minute", "brother"]
            response += " " + random.choice(fillers)
        
        return response[:500]

# Global instance
agent_orchestrator = AgentOrchestrator()