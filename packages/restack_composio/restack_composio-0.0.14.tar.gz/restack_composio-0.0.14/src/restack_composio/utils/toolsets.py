from composio_openai import ComposioToolSet

def openai_toolset(entity_id: str) -> ComposioToolSet:
    return ComposioToolSet(entity_id=entity_id)
