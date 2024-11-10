from restack_ai import Restack
from pydantic import BaseModel
from .functions.chat.completions_base import openai_chat_completion_base
from .task_queue import openai_task_queue
class OpenAIServiceOptions(BaseModel):
    rate_limit: int

class RestackWrapper(BaseModel):
    client: Restack
    
    class Config:
        arbitrary_types_allowed = True


class OpenAIServiceInput(BaseModel):
    client: RestackWrapper
    options: OpenAIServiceOptions

async def openai_service(input: OpenAIServiceInput):
    return await input.client.start_service(
        functions=[
            openai_chat_completion_base,
        ],
        task_queue=openai_task_queue,
        options=input.options
    )

if __name__ == "__main__":
    openai_service(
        client=Restack(),
        options=OpenAIServiceOptions(rate_limit=100000)
    )
