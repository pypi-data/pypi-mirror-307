from pydantic import BaseModel
from typing import List, Dict
import google.generativeai as genai

class GeminiGetHistoryInput(BaseModel):
    chat: genai.ChatSession
    model_config = {
        "arbitrary_types_allowed": True
    }    

def gemini_get_history(input: GeminiGetHistoryInput) -> List[Dict]:
    """
    Returns a serialized version of the chat history.
    
    Returns:
        List[Dict]: List of messages, each containing 'role' and 'parts' keys
    """
    return [
        {
            "role": msg.role,
            "parts": [part.text for part in msg.parts]
        }
        for msg in input.chat.history
    ]