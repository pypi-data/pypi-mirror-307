from restack_ai import Restack
from pydantic import BaseModel
from .functions.generate_content import gemini_generate_content
from .task_queue import gemini_task_queue

class GeminiServiceOptions(BaseModel):
    rate_limit: int

class RestackWrapper(BaseModel):
    client: Restack
    
    class Config:
        arbitrary_types_allowed = True


class GeminiServiceInput(BaseModel):
    client: RestackWrapper
    options: GeminiServiceOptions


async def gemini_service(input: GeminiServiceInput):
    return await input.client.start_service(
        functions=[
            gemini_generate_content
        ],
        task_queue=gemini_task_queue,
        options=input.options
    )

if __name__ == "__main__":
    gemini_service(
        client=Restack(),
        options=GeminiServiceOptions(rate_limit=100000)
    )
