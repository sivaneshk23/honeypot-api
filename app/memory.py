import threading
import time
from datetime import datetime
from collections import OrderedDict

class ConversationMemory:
    """Simple conversation memory"""
    
    def __init__(self, max_conversations: int = 1000):
        self.memory = OrderedDict()
        self.max_size = max_conversations
        self.lock = threading.RLock()
    
    def get_conversation(self, conversation_id: str) -> dict:
        """Get or create conversation"""
        with self.lock:
            if conversation_id in self.memory:
                data = self.memory[conversation_id]
                data["last_accessed"] = datetime.utcnow()
                self.memory.move_to_end(conversation_id)
                return data
            
            # Evict if needed
            if len(self.memory) >= self.max_size:
                self.memory.popitem(last=False)
            
            new_conv = {
                "id": conversation_id,
                "created": datetime.utcnow(),
                "last_accessed": datetime.utcnow(),
                "turns": 0,
                "start_time": time.time()
            }
            
            self.memory[conversation_id] = new_conv
            return new_conv
    
    def update_turns(self, conversation_id: str):
        """Update turn count"""
        with self.lock:
            if conversation_id in self.memory:
                self.memory[conversation_id]["turns"] += 1
                self.memory[conversation_id]["last_accessed"] = datetime.utcnow()

# Global instance
conversation_memory = ConversationMemory()