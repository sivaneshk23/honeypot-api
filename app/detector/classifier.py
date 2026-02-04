import re

class ScamClassifier:
    """Simple scam detection"""
    
    def __init__(self):
        self.scam_keywords = [
            'won', 'win', 'winner', 'lottery', 'prize', 'reward',
            'urgent', 'immediate', 'emergency', 'payment', 'transfer',
            'account', 'bank', 'upi', 'password', 'otp', 'pin',
            'click', 'visit', 'link', 'website', 'verify',
            'free', 'gift', 'bonus', 'claim', 'collect',
            'government', 'official', 'authority', 'fund', 'scheme',
            'suspend', 'block', 'close', 'secure', 'authenticate'
        ]
    
    def detect_scam(self, text: str) -> tuple:
        """Detect scam with confidence"""
        text_lower = text.lower()
        
        # Count scam keywords
        scam_count = 0
        for keyword in self.scam_keywords:
            if keyword in text_lower:
                scam_count += 1
        
        # Check for URLs
        has_url = bool(re.search(r'https?://\S+', text_lower))
        
        # Check for phone numbers
        has_phone = bool(re.search(r'(\+91[\-\s]?)?[6-9]\d{9}', text))
        
        # Calculate confidence
        confidence = min((scam_count * 0.1) + (0.3 if has_url else 0) + (0.2 if has_phone else 0), 1.0)
        
        # Decision
        is_scam = confidence >= 0.4
        
        return is_scam, confidence

# Global instance
scam_classifier = ScamClassifier()