import re

class IntelligenceExtractor:
    """Extract intelligence from text"""
    
    def __init__(self):
        self.patterns = {
            "bank_account": [
                (r'\b\d{9,18}\b', 0.7),
                (r'account\s*(?:no|number|#)?\s*[:=]?\s*(\d{9,18})', 0.9)
            ],
            "upi_id": [
                (r'\b[\w.\-]{2,}@(?:okicici|okhdfc|okaxis|oksbi|ybl|axl|ibl)\b', 0.95),
                (r'upi\s*(?:id)?\s*[:=]?\s*([\w.\-]{2,}@[a-zA-Z]{2,})', 0.9)
            ],
            "url": [
                (r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*', 0.8),
                (r'(?:click|visit|open)\s*(?:this|the)?\s*(?:link|url|website)\s*[:=]?\s*(https?://\S+)', 0.95)
            ]
        }
    
    def extract_all(self, text: str) -> dict:
        """Extract all intelligence"""
        results = {
            "bank_accounts": [],
            "upi_ids": [],
            "urls": []
        }
        
        for item_type, patterns in self.patterns.items():
            for pattern, confidence in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    groups = match.groups()
                    value = groups[0] if groups and groups[0] else match.group(0)
                    
                    if value:
                        results[f"{item_type}s"].append({
                            "value": value.strip(),
                            "confidence": confidence
                        })
        
        # Remove duplicates
        for key in results:
            seen = set()
            unique = []
            for item in results[key]:
                if item["value"] not in seen:
                    seen.add(item["value"])
                    unique.append(item)
            results[key] = unique
        
        return results

# Global instance
intelligence_extractor = IntelligenceExtractor()