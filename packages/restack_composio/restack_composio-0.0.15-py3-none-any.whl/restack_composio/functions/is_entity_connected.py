from composio import  App
from composio.client.exceptions import NoItemsFound
from .get_entity import get_entity, GetEntityInput
from pydantic import BaseModel

class IsEntityConnectedInput(BaseModel):
    entity_id: str
    appType: str
    composio_api_key: str | None = None

def is_entity_connected(input: IsEntityConnectedInput):
    entity = get_entity(input=GetEntityInput(entity_id=input.entity_id, composio_api_key=input.composio_api_key))
    app_enum = getattr(App, input.appType)

    try:
        entity_connection = entity.get_connection(app=app_enum)
        return entity_connection
    except NoItemsFound as e:
        return False
