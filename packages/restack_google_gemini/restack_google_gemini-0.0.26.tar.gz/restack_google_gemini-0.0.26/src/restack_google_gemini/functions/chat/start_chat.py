from pydantic import BaseModel
import google.generativeai as genai

class GeminiStartChatInput(BaseModel):
    model: str
    api_key: str
    generation_config: dict | None = None
    history: list[dict] | None = None

def gemini_start_chat(input: GeminiStartChatInput):
    if not input.api_key:
        raise ValueError("api_key is required")
    
    genai.configure(api_key=input.api_key)

    model = genai.GenerativeModel(
        model_name=input.model,
        generation_config=genai.GenerationConfig(**input.generation_config)
    )

    chat = model.start_chat(
        history=input.history
    )

    return chat
