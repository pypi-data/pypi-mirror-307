from restack_ai import Restack
from pydantic import BaseModel
from .functions.send_email import mail_website_summary
from .functions.summarize_website import summarize_website
from .task_queue import toolhouse_task_queue
class ToolhouseServiceOptions(BaseModel):
    rate_limit: int

class RestackWrapper(BaseModel):
    client: Restack
    
    class Config:
        arbitrary_types_allowed = True


class ToolhouseServiceInput(BaseModel):
    client: RestackWrapper
    options: ToolhouseServiceOptions


async def toolhouse_service(input: ToolhouseServiceInput):
    return await input.client.start_service(
        functions=[
            mail_website_summary,
            summarize_website
        ],
         task_queue=toolhouse_task_queue,
        options=input.options
    )

if __name__ == "__main__":
    toolhouse_service(
        client=Restack(),
        options=ToolhouseServiceOptions(rate_limit=100000)
    )
