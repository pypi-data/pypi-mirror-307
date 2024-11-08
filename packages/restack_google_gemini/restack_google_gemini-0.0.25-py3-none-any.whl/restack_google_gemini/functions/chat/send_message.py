from pydantic import BaseModel
import google.generativeai as genai

class GeminiSendMessageInput(BaseModel):
    user_content: str
    chat: genai.ChatSession
    model_config = {
        "arbitrary_types_allowed": True
    }

def gemini_send_message(input: GeminiSendMessageInput):
    return input.chat.send_message(input.user_content)

