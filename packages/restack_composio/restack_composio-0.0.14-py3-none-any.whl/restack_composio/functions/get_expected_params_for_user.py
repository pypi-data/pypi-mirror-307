from composio import ComposioToolSet, App   

def get_expected_params_for_user(app: App):
    toolset = ComposioToolSet()
    return toolset.get_expected_params_for_user(app=app)
