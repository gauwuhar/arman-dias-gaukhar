import dialogflow_v2 as dialogflow # type: ignore
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = 'your-project-id'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'current-session-id'

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

def send_to_dialogflow(text):
    text_input = dialogflow.types.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except InvalidArgument:
        raise

def process_user_message(message):
    # Sending user message to Dialogflow and getting the response
    return send_to_dialogflow(message)
