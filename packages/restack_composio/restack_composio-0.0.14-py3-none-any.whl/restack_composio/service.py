from restack_ai import Restack
from pydantic import BaseModel
from .functions.create_calendar_event import create_calendar_event
from .functions.get_entity import get_entity
from .functions.get_expected_params_for_user import get_expected_params_for_user
from .functions.initiate_connection import initiate_connection
from .functions.is_entity_connected import is_entity_connected
from .task_queue import composio_task_queue
class ComposioServiceOptions(BaseModel):
    rate_limit: int

class RestackWrapper(BaseModel):
    client: Restack
    
    class Config:
        arbitrary_types_allowed = True


class ComposioServiceInput(BaseModel):
    client: RestackWrapper
    options: ComposioServiceOptions


async def composio_service(input: ComposioServiceInput):
    return await input.client.start_service(
        functions=[
            create_calendar_event,
            get_entity,
            get_expected_params_for_user,
            initiate_connection,
            is_entity_connected
        ],
        task_queue=composio_task_queue,
        options=input.options
    )

if __name__ == "__main__":
    composio_service(
        client=Restack(),
        options=ComposioServiceOptions(rate_limit=100000)
    )
