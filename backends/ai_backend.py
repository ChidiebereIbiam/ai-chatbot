# ai_backend.py
import time
import random

class ChatAI:
    """Simple AI backend that can be replaced with more advanced models."""
    
    def __init__(self):
        # Could initialize more complex AI models here
        self.responses = {
            "greeting": ["Hello!", "Hi there!", "Hey, how can I help today?"],
            "farewell": ["Goodbye!", "See you later!", "Have a great day!"],
            "thanks": ["You're welcome!", "No problem!", "Glad I could help!"],
            "default": ["I see.", "That's interesting.", "Tell me more about that."]
        }
        
    def get_response(self, user_message):
        """Generate a response to the user's message."""
        # Simulate thinking time
        time.sleep(0.5)
        
        # Simple keyword matching (could be replaced with actual NLP)
        user_message = user_message.lower()
        
        if any(word in user_message for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["greeting"])
        elif any(word in user_message for word in ["bye", "goodbye", "see you"]):
            return random.choice(self.responses["farewell"])
        elif any(word in user_message for word in ["thanks", "thank you"]):
            return random.choice(self.responses["thanks"])
        elif "?" in user_message:
            return "That's a good question. Let me think about it..."
        else:
            # Here you would integrate with a real AI model
            return f"I processed your message: '{user_message}' and would provide an intelligent response here."

# Singleton instance
ai = ChatAI()

def process_message(message):
    """Process a message and get AI response."""
    return ai.get_response(message)
