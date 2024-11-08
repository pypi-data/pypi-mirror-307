from ..utils.client import composio_toolset, ComposioToolSetInput

from pydantic import BaseModel

class GetEntityInput(BaseModel):
    composio_api_key: str | None = None
    entity_id: str

def get_entity(input: GetEntityInput):
    toolset = composio_toolset(ComposioToolSetInput(
        composio_api_key=input.composio_api_key,
        entity_id=input.entity_id
    ))
    return toolset.get_entity()
