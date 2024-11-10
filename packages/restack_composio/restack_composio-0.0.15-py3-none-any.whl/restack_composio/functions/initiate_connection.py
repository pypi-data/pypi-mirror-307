from restack_ai.function import FunctionFailure
from .get_entity import get_entity, GetEntityInput
from typing import Optional
from pydantic import BaseModel
from .is_entity_connected import is_entity_connected, IsEntityConnectedInput

class InitiateConnectionInput(BaseModel):
    entity_id: str
    app_name: str
    composio_api_key: Optional[str] = None
    wait_until_active: Optional[int] = None
def initiate_connection(
    input: InitiateConnectionInput
):
    try:
        entity = get_entity(GetEntityInput(
            composio_api_key=input.composio_api_key,
            entity_id=input.entity_id
        ))

        entity_is_connected = is_entity_connected(input=IsEntityConnectedInput(
            entity_id=input.entity_id,
            appType=input.app_name,
            composio_api_key=input.composio_api_key
        ))

        if (entity_is_connected):
           response = {
            "authenticated": "yes",
            "message": f"User {input.entity_id} is already authenticated with {input.app_name}.",
            "url": ""
           }
           return response

        request =  entity.initiate_connection(app_name=input.app_name)

        if (input.wait_until_active):
            request.wait_until_active(client=entity.client, timeout=input.wait_until_active)
            response = {
                "authenticated": "yes",
                "message": f"User {input.entity_id} is authenticated with {input.app_name}.",
                "url": ""
            }
            return response
        else:
            response = {
                "authenticated": "no",
                "message": f"User {input.entity_id} is not yet authenticated with {input.app_name}. Please authenticate.",
                "url": request.redirectUrl
            }
            return response

    except Exception as error:
        raise FunctionFailure(
            f"Error initiating connection: {error}",
            non_retryable=True
        )
