from pydantic import BaseModel
import google.generativeai as genai

class GeminiGenerateContentInput(BaseModel):
    user_content: str
    model: str | None = None
    api_key: str = ""
    generation_config: dict | None = None
    system_instruction: str | None = None
    
def gemini_generate_content(input) :
    if not input.api_key:
        raise ValueError("api_key is required")
    
    genai.configure(api_key=input.api_key)

    model = genai.GenerativeModel(model_name=input.model, system_instruction=input.system_instruction)

    response = model.generate_content(input.user_content, generation_config=genai.GenerationConfig(**input.generation_config))

    return response.text

