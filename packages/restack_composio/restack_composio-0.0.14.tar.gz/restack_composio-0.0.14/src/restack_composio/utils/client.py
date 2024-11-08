from composio import ComposioToolSet
from pydantic import BaseModel
import os

class ComposioToolSetInput(BaseModel):
    composio_api_key: str | None = None
    entity_id: str

def composio_toolset(input: ComposioToolSetInput) -> ComposioToolSet:
    api_key = input.composio_api_key or os.getenv('COMPOSIO_API_KEY')
    return ComposioToolSet(api_key=api_key, entity_id=input.entity_id)
