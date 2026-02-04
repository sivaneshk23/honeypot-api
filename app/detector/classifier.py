import re
import math
from typing import Dict, List, Tuple, Set
import hashlib

class WorldClassScamDetector:
    """World's Best Scam Detection System - GUVI HCL Hackathon"""
    
    def __init__(self):
        # Multi-level keyword scoring
        self.keyword_categories = {
            "financial_scam": {
                'won': 1.0, 'win': 1.0, 'winner': 1.0, 'lottery': 1.0, 'prize': 1.0,
                'reward': 0.9, 'jackpot': 1.0, 'bonanza': 1.0, 'fortune': 0.9,
                'million': 0.9, 'crore': 0.9, 'lakh': 0.8, 'cash': 0.8, 'money': 0.7
            },
            "urgency_pressure": {
                'urgent': 0.9, 'immediate': 0.9, 'emergency': 0.9, 'now': 0.8,
                'today': 0.8, 'quick': 0.7, 'fast': 0.7, 'hurry': 0.9,
                'limited': 0.8, 'expire': 0.9, 'deadline': 0.8, 'last chance': 1.0,
                'final': 0.8, 'instant': 0.8, 'right now': 1.0
            },
            "authority_impersonation": {
                'government': 0.9, 'official': 0.9, 'authority': 0.9, 'income tax': 1.0,
                'itr': 0.8, 'tax': 0.8, 'court': 0.9, 'police': 0.9, 'cid': 0.8,
                'cyber crime': 0.9, 'rbi': 1.0, 'sebi': 0.9, 'bank official': 1.0,
                'manager': 0.7, 'officer': 0.7, 'agent': 0.7
            },
            "financial_threats": {
                'block': 1.0, 'suspend': 1.0, 'freeze': 0.9, 'close': 0.9,
                'deactivate': 0.8, 'terminate': 0.8, 'penalty': 0.9, 'fine': 0.9,
                'legal action': 1.0, 'arrest': 1.0, 'case': 0.8, 'complaint': 0.8,
                'fraud': 0.9, 'scam': 0.9, 'investigation': 0.8
            },
            "payment_demand": {
                'send money': 1.0, 'transfer': 0.9, 'pay': 0.9, 'deposit': 0.9,
                'credit': 0.8, 'account': 0.8, 'bank': 0.8, 'upi': 1.0,
                'google pay': 0.9, 'phonepe': 0.9, 'paytm': 0.9, 'net banking': 0.8,
                'rtgs': 0.7, 'neft': 0.7, 'imps': 0.7
            },
            "personal_info": {
                'password': 1.0, 'otp': 1.0, 'pin': 1.0, 'aadhaar': 1.0,
                'pan': 1.0, 'card': 0.9, 'cvv': 1.0, 'expiry': 0.8,
                'signature': 0.7, 'photo': 0.6, 'document': 0.7,
                'kyc': 0.9, 'verification': 0.8, 'authenticate': 0.8
            },
            "call_to_action": {
                'click': 0.9, 'visit': 0.8, 'open': 0.7, 'call': 0.7,
                'message': 0.6, 'whatsapp': 0.8, 'telegram': 0.7,
                'download': 0.8, 'install': 0.7, 'update': 0.7,
                'verify': 0.8, 'confirm': 0.7, 'submit': 0.7
            },
            "free_offers": {
                'free': 0.8, 'gift': 0.8, 'bonus': 0.8, 'offer': 0.7,
                'discount': 0.6, 'coupon': 0.6, 'voucher': 0.6,
                'gift card': 0.8, 'shopping': 0.5, 'amazon': 0.6,
                'flipkart': 0.6, 'voucher': 0.6
            }
        }
        
        # Common scam patterns
        self.scam_patterns = [
            (r'(won|win|winner).*?(lottery|prize|reward).*?(\d+[,\s]*(lakh|crore|million|thousand))', 1.0),
            (r'(urgent|emergency).*?(account|bank).*?(block|suspend)', 1.0),
            (r'(government|official|rbi|income tax).*?(fine|penalty|payment)', 0.9),
            (r'(send|transfer|pay).*?(money|amount).*?(account|upi|bank)', 0.9),
            (r'(click|visit).*?(link|website|url).*?(verify|confirm)', 0.8),
            (r'(free|gift|bonus).*?(claim|collect).*?(offer)', 0.7),
            (r'(password|otp|pin|cvv).*?(share|send|provide)', 1.0),
            (r'(aadhaar|pan|document).*?(update|verify|submit)', 0.8)
        ]
        
        # Known scam URLs
        self.known_scam_domains = {
            'bit\.ly', 'tinyurl\.com', 'short\.url', 'cutt\.ly',
            'rebrand\.ly', 'is\.gd', 'clck\.ru', 'shorte\.st',
            'adf\.ly', 'ouo\.io', 'bc\.vc', 'goo\.gl'
        }
        
        # Suspicious TLDs
        self.suspicious_tlds = {'.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club'}
    
    def calculate_linguistic_features(self, text: str) -> Dict:
        """Analyze linguistic patterns"""
        features = {
            "exclamation_ratio": 0,
            "caps_ratio": 0,
            "urgency_words": 0,
            "emotional_words": 0,
            "length_score": 0
        }
        
        if not text:
            return features
        
        # Exclamation analysis
        exclamation_count = text.count('!')
        features["exclamation_ratio"] = min(exclamation_count / 5, 1.0)
        
        # CAPS analysis
        words = text.split()
        if words:
            caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)
            features["caps_ratio"] = min(caps_words / len(words), 1.0)
        
        # Urgency words
        urgency_keywords = {'urgent', 'immediate', 'emergency', 'now', 'today', 'hurry', 'quick'}
        features["urgency_words"] = sum(1 for word in urgency_keywords if word in text.lower())
        
        # Emotional words
        emotional_words = {'congratulations', 'alert', 'warning', 'danger', 'important', 'attention'}
        features["emotional_words"] = sum(1 for word in emotional_words if word in text.lower())
        
        # Length score (very short or very long are suspicious)
        features["length_score"] = 0.7 if len(text) < 20 or len(text) > 500 else 0.0
        
        return features
    
    def analyze_urls(self, text: str) -> float:
        """Analyze URLs in text"""
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text.lower())
        
        if not urls:
            return 0.0
        
        url_score = 0.0
        
        for url in urls:
            # Check for known scam domains
            for domain in self.known_scam_domains:
                if re.search(domain, url):
                    url_score = max(url_score, 0.9)
                    break
            
            # Check for suspicious TLDs
            for tld in self.suspicious_tlds:
                if tld in url:
                    url_score = max(url_score, 0.8)
                    break
            
            # Check for IP addresses
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                url_score = max(url_score, 0.7)
            
            # URL shortening detection
            if len(url) < 30 and 'http' in url:
                url_score = max(url_score, 0.6)
        
        return url_score
    
    def detect_phone_numbers(self, text: str) -> float:
        """Detect and analyze phone numbers"""
        # Indian phone numbers
        indian_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'
        numbers = re.findall(indian_pattern, text)
        
        if not numbers:
            return 0.0
        
        # Multiple numbers are more suspicious
        if len(numbers) > 1:
            return 0.8
        
        # Number in suspicious context
        suspicious_contexts = ['call', 'whatsapp', 'message', 'contact', 'number is']
        context_found = any(context in text.lower() for context in suspicious_contexts)
        
        return 0.7 if context_found else 0.4
    
    def analyze_financial_info(self, text: str) -> float:
        """Analyze financial information patterns"""
        score = 0.0
        
        # Bank account patterns
        if re.search(r'\b\d{9,18}\b', text):
            score = max(score, 0.7)
            # With keywords
            if any(keyword in text.lower() for keyword in ['account', 'bank', 'acc']):
                score = max(score, 0.9)
        
        # UPI ID patterns
        upi_patterns = [
            r'[\w.\-]+@(okicici|okhdfc|okaxis|oksbi|ybl|axl|ibl)',
            r'upi[\s:]+[\w.\-]+@[\w]+',
            r'pay[\s]+to[\s]+[\w.\-]+@[\w]+'
        ]
        
        for pattern in upi_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score = max(score, 0.95)
                break
        
        # Card number patterns
        if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text):
            score = max(score, 1.0)
        
        return score
    
    def calculate_pattern_score(self, text: str) -> float:
        """Calculate pattern matching score"""
        pattern_score = 0.0
        
        for pattern, weight in self.scam_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                pattern_score = max(pattern_score, weight)
        
        return pattern_score
    
    def calculate_keyword_score(self, text: str) -> Dict:
        """Calculate comprehensive keyword scores"""
        text_lower = text.lower()
        category_scores = {}
        
        for category_name, keywords in self.keyword_categories.items():
            category_score = 0.0
            found_keywords = []
            
            for keyword, weight in keywords.items():
                if keyword in text_lower:
                    category_score += weight
                    found_keywords.append(keyword)
            
            # Normalize category score
            if found_keywords:
                category_score = min(category_score / 3, 1.0)
            
            category_scores[category_name] = {
                "score": category_score,
                "keywords": found_keywords[:5]  # Limit to top 5
            }
        
        return category_scores
    
    def detect_scam(self, text: str) -> Tuple[bool, float, Dict]:
        """World-class scam detection with detailed analysis"""
        if not text or len(text.strip()) < 3:
            return False, 0.0, {}
        
        text_lower = text.lower()
        
        # 1. Calculate keyword scores
        keyword_analysis = self.calculate_keyword_score(text_lower)
        keyword_score = max(cat["score"] for cat in keyword_analysis.values())
        
        # 2. Pattern matching
        pattern_score = self.calculate_pattern_score(text_lower)
        
        # 3. URL analysis
        url_score = self.analyze_urls(text_lower)
        
        # 4. Phone number analysis
        phone_score = self.detect_phone_numbers(text)
        
        # 5. Financial info analysis
        financial_score = self.analyze_financial_info(text_lower)
        
        # 6. Linguistic features
        linguistic = self.calculate_linguistic_features(text)
        linguistic_score = (
            linguistic["exclamation_ratio"] * 0.3 +
            linguistic["caps_ratio"] * 0.2 +
            min(linguistic["urgency_words"] * 0.2, 0.4) +
            min(linguistic["emotional_words"] * 0.1, 0.3) +
            linguistic["length_score"] * 0.2
        )
        
        # 7. Combined score calculation with weights
        scores = {
            "keyword": keyword_score * 0.35,
            "pattern": pattern_score * 0.25,
            "financial": financial_score * 0.20,
            "url": url_score * 0.10,
            "phone": phone_score * 0.05,
            "linguistic": linguistic_score * 0.05
        }
        
        total_confidence = sum(scores.values())
        
        # 8. Boost for critical combinations
        critical_combinations = [
            ("financial_scam", "payment_demand"),
            ("urgency_pressure", "financial_threats"),
            ("authority_impersonation", "payment_demand")
        ]
        
        for cat1, cat2 in critical_combinations:
            if (keyword_analysis[cat1]["score"] > 0.6 and 
                keyword_analysis[cat2]["score"] > 0.6):
                total_confidence = min(total_confidence + 0.2, 1.0)
                break
        
        # 9. Decision threshold (adaptive)
        # Lower threshold if any critical element is present
        threshold = 0.4
        if financial_score > 0.7 or pattern_score > 0.8:
            threshold = 0.35
        
        is_scam = total_confidence >= threshold
        
        # 10. Detailed analysis report
        analysis_report = {
            "confidence": total_confidence,
            "threshold_used": threshold,
            "category_scores": {k: v["score"] for k, v in keyword_analysis.items()},
            "detected_patterns": {
                "urls_found": url_score > 0,
                "phone_found": phone_score > 0,
                "financial_info": financial_score > 0
            },
            "linguistic_features": linguistic,
            "component_scores": scores,
            "decision_factors": []
        }
        
        # Add decision factors
        if keyword_score > 0.7:
            analysis_report["decision_factors"].append("high_keyword_match")
        if financial_score > 0.8:
            analysis_report["decision_factors"].append("financial_info_detected")
        if pattern_score > 0.7:
            analysis_report["decision_factors"].append("known_scam_pattern")
        
        print(f"🔍 ULTIMATE DETECTION ANALYSIS:")
        print(f"   Text: '{text[:80]}...'")
        print(f"   Total Confidence: {total_confidence:.2f}")
        print(f"   Threshold: {threshold:.2f}")
        print(f"   Decision: {'SCAM' if is_scam else 'LEGIT'}")
        print(f"   Key Scores: K={keyword_score:.2f}, P={pattern_score:.2f}, F={financial_score:.2f}")
        print(f"   Factors: {analysis_report['decision_factors']}")
        
        return is_scam, total_confidence, analysis_report

# Global instance
scam_detector = WorldClassScamDetector()

# Backward compatibility function
def detect_scam(text: str) -> tuple:
    """Legacy interface for backward compatibility"""
    is_scam, confidence, _ = scam_detector.detect_scam(text)
    return is_scam, confidence