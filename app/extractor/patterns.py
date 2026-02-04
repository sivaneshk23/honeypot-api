import re
import json
from typing import Dict, List, Any
from urllib.parse import urlparse

class EliteIntelligenceExtractor:
    """Elite Intelligence Extraction System"""
    
    def __init__(self):
        # Enhanced patterns with context awareness
        self.patterns = {
            "bank_account": [
                # Standard account numbers
                (r'(?:account|acc|ac)\s*(?:no|number|#|no\.)?\s*[:=\-]?\s*(\d{9,18})', 0.95),
                (r'\b(\d{9,18})\b(?=\s*(?:is|for|of|in|to|from|account|bank))', 0.85),
                (r'bank\s+(?:account|details)\s*[:=\-]?\s*(\d{9,18})', 0.98),
                # With bank names
                (r'(?:sbi|hdfc|icici|axis|kotak|pnb)\s+(?:account|acc)\s*[:=\-]?\s*(\d{9,18})', 0.99),
            ],
            "upi_id": [
                # Standard UPI patterns
                (r'\b([\w.\-]{2,}@(?:okicici|okhdfc|okaxis|oksbi|ybl|axl|ibl|upi|paytm))\b', 0.97),
                (r'upi\s*(?:id|address)?\s*[:=\-]?\s*([\w.\-]+@[\w.]+)', 0.96),
                (r'pay\s*(?:to|via)?\s*([\w.\-]+@[\w.]+)', 0.94),
                (r'send\s+(?:money|payment|amount)\s+to\s+([\w.\-]+@[\w.]+)', 0.98),
                # Phone number as UPI
                (r'(\d{10})@(?:okicici|okhdfc|okaxis|oksbi|ybl|axl)', 0.95),
            ],
            "url": [
                # Complete URL patterns
                (r'(?:https?://|www\.)[^\s<>"\'{}|\\^`\[\]]+', 0.9),
                (r'(?:click|visit|open|go to|check)\s+(?:this|the|our)?\s*(?:link|site|website|page|portal)\s*[:=\-]?\s*((?:https?://|www\.)[^\s]+)', 0.97),
                # Shortened URLs
                (r'(?:bit\.ly|tinyurl\.com|short\.url|cutt\.ly|rebrand\.ly)/[^\s]+', 0.85),
                # Payment links
                (r'(?:pay|payment|buy|purchase|donate)\s*(?:link|url)?\s*[:=\-]?\s*(https?://[^\s]+)', 0.95),
            ],
            "phone_number": [
                # Indian numbers
                (r'(?:\+91[\-\s]?)?[6-9]\d{9}', 0.8),
                (r'contact\s*(?:no|number)?\s*[:=\-]?\s*((?:\+91[\-\s]?)?[6-9]\d{9})', 0.9),
                (r'call\s+(?:me|us|at)?\s*[:=\-]?\s*((?:\+91[\-\s]?)?[6-9]\d{9})', 0.88),
                (r'whatsapp\s*(?:no|number)?\s*[:=\-]?\s*((?:\+91[\-\s]?)?[6-9]\d{9})', 0.92),
            ],
            "email": [
                # Email addresses
                (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 0.8),
                (r'email\s*(?:id|address)?\s*[:=\-]?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', 0.9),
            ],
            "card_details": [
                # Credit/Debit cards
                (r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', 0.99),
                (r'(?:card|credit|debit)\s+(?:no|number)\s*[:=\-]?\s*(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4})', 1.0),
                (r'cvv\s*[:=\-]?\s*(\d{3,4})', 0.95),
                (r'expir(?:y|ation)\s*(?:date)?\s*[:=\-]?\s*(\d{2}/\d{2,4})', 0.9),
            ]
        }
        
        # Context validation rules
        self.context_rules = {
            "bank_account": lambda text, match: any(word in text.lower() for word in ['account', 'bank', 'transfer', 'send']),
            "upi_id": lambda text, match: any(word in text.lower() for word in ['upi', 'pay', 'send money', 'transfer']),
            "url": lambda text, match: any(word in text.lower() for word in ['click', 'visit', 'link', 'website']),
        }
        
        # False positive filters
        self.false_positive_filters = {
            "bank_account": [
                lambda x: len(x) < 9,  # Too short
                lambda x: len(set(x)) < 3,  # Too repetitive (111111111)
                lambda x: x.startswith('0') and len(x) > 10,  # Likely not account
            ],
            "phone_number": [
                lambda x: x in ['9999999999', '8888888888', '9876543210'],  # Test numbers
            ]
        }
    
    def clean_value(self, value: str, pattern_type: str) -> str:
        """Clean extracted values"""
        if not value:
            return value
        
        # Remove common punctuation
        value = value.strip(' .,;:!?\'"[]{}()<>')
        
        # Type-specific cleaning
        if pattern_type == "bank_account":
            # Remove non-digits
            value = re.sub(r'\D', '', value)
        elif pattern_type == "upi_id":
            # Ensure proper format
            value = value.lower()
        elif pattern_type == "url":
            # Ensure http prefix
            if not value.startswith(('http://', 'https://', 'www.')):
                value = 'http://' + value
        
        return value
    
    def is_false_positive(self, value: str, pattern_type: str) -> bool:
        """Check if extracted value is likely false positive"""
        if pattern_type in self.false_positive_filters:
            for filter_func in self.false_positive_filters[pattern_type]:
                if filter_func(value):
                    return True
        return False
    
    def has_context(self, text: str, match: str, pattern_type: str) -> bool:
        """Check if match has proper context"""
        if pattern_type in self.context_rules:
            return self.context_rules[pattern_type](text, match)
        return True
    
    def extract_all(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all intelligence with validation"""
        results = {
            "bank_accounts": [],
            "upi_ids": [],
            "urls": [],
            "phone_numbers": [],
            "emails": [],
            "card_details": []
        }
        
        if not text or len(text.strip()) < 10:
            return results
        
        for pattern_type, patterns in self.patterns.items():
            for pattern, confidence in patterns:
                try:
                    matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        groups = match.groups()
                        value = groups[0] if groups and groups[0] else match.group(0)
                        
                        if value:
                            value = self.clean_value(value, pattern_type)
                            
                            # Validate
                            if not value or self.is_false_positive(value, pattern_type):
                                continue
                            
                            if not self.has_context(text, value, pattern_type):
                                confidence *= 0.7  # Reduce confidence for missing context
                            
                            # Add to results
                            result_key = f"{pattern_type.replace('_', '')}s"
                            if result_key in results:
                                results[result_key].append({
                                    "value": value,
                                    "confidence": confidence,
                                    "context": match.group(0)[:50]
                                })
                except Exception as e:
                    print(f"Pattern error in {pattern_type}: {e}")
                    continue
        
        # Remove duplicates (same value)
        for key in results:
            seen = set()
            unique = []
            for item in results[key]:
                if item["value"] not in seen:
                    seen.add(item["value"])
                    unique.append(item)
            results[key] = sorted(unique, key=lambda x: x["confidence"], reverse=True)
        
        # Filter low confidence results
        for key in results:
            results[key] = [item for item in results[key] if item["confidence"] >= 0.6]
        
        print(f"🔍 ELITE EXTRACTION RESULTS:")
        for key, items in results.items():
            if items:
                print(f"   {key}: {len(items)} items")
                for item in items[:3]:  # Show top 3
                    print(f"     - {item['value']} (conf: {item['confidence']:.2f})")
        
        return results

# Global instance
intelligence_extractor = EliteIntelligenceExtractor()