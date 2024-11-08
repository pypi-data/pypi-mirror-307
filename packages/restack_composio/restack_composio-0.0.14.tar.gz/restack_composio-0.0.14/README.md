### Composio Restack AI integration

This integration can be used in your project to interact with Composio.
Currently you get 4 functions exposed for your usage.

1. create_calendar_event. This function can be used as an example on how to interact with toolhouse. It will create an event on the google calendar of the connected account in the entity provided.
2. get_entity. This function will return the entity based on the entity_id provided
3. get_expected_params_for_user. This function returns the parameters needed for a user to initiate a connection. This is helpful in cases like shopify connection where user needs to provide tokens. Use this function to get list of fields and then you can decide how you want to fetch this from the end user.
4. initiate_connection. This function will initiate a connection to the provided app. In case a connection is on initiated state the connection object will be returned in which it contains the redirect url the user needs to visit in order to complete auth flow. For example for google calendar user needs to linked their google account in order for the composio tool to be able to create an event on the calendar.
5. is_entity_connected. Will help you determine if the entity is already connected to an application.

### Notes

Make sure to create an account in composio and on your project set the COMPOSIO_API_KEY as an environment variable.
