from flask import Flask, request, jsonify
from pymongo import MongoClient
from google.cloud import dialogflow_v2 as dialogflow
from flask_cors import CORS
import os
import joblib

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the database client and connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.chatbot_db

# Dialogflow setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'path_to_google_credentials.json'
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = 'your_project_id_here'

def detect_intent_texts(text, session_id, language_code='en'):
    """Detect intent with text input using Dialogflow.

    Args:
        text (str): The text to classify.
        session_id (str): The unique identifier of the user's session.
        language_code (str, optional): The language code of the text. Defaults to 'en'.

    Returns:
        dialogflow.types.queryresult.QueryResult: The results of the Dialogflow query.
    """
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    # The text input.
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    # The input for the Dialogflow query.
    query_input = dialogflow.QueryInput(text=text_input)
    # Send the request to the Dialogflow API.
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    # Return the results of the query.
    return response.query_result


@app.route('/message', methods=['POST'])
def handle_message():
    """
    Handle incoming messages and respond with Dialogflow intent.

    This function receives a JSON object with a message and a session ID
    from the client, uses the Dialogflow API to get the intent and
    fulfillment text for the message, and responds with the fulfillment text.

    Additionally, this function saves the conversation to MongoDB for
    future reference.
    """
    message = request.json['message']
    session_id = request.json['session_id']
    response = detect_intent_texts(message, session_id)

    # Process Dialogflow response
    # Add any additional processing based on the response here

    # Save the conversation to MongoDB
    db.conversations.insert_one({
        'session_id': session_id,
        'text': message,
        'intent': response.intent.display_name,
        'response': response.fulfillment_text
    })

    # Respond with Dialogflow's fulfillment text
    return jsonify({'message': response.fulfillment_text})

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    # Process the message with Dialogflow or your NLP model
    response_message = process_message(user_message)
    return jsonify({'message': response_message})

def process_message(message):
    # This function would handle talking to Dialogflow or another service
    # and generating a response based on the user's message.
    # Replace this with your actual logic to get a response.
    return "Response from your chatbot"

@app.route('/api/dialogflow', methods=['POST'])
def dialogflow_route():
    data = request.json
    user_input = data['message']

    # Process the input with Dialogflow or any other logic
    reply = process_with_dialogflow(user_input)

    # Return the reply in JSON format
    return jsonify({'reply': reply})

def process_with_dialogflow(message):
    # Assume we have a function that sends the user message to Dialogflow and gets a response
    response = send_message_to_dialogflow(message)
    return response

# Placeholder for Dialogflow interaction
def send_message_to_dialogflow(message):
    # Use the Dialogflow client to send a message and return the response
    # Here we return a static response for example purposes
    return "This is a response from Dialogflow"

@app.route('/routes', methods=['GET'])
def get_routes():
    """Get route recommendations based on user preferences."""
    # Get user preferences from request
    preferences = request.args
    print(preferences)
    # Implement route recommendation logic here
    # Get mode of transportation preference from request
    mode = preferences.get('mode')
    # If the user provided a preference for transportation mode
    if mode:
        # Recommend routes based on mode of transportation
        routes = get_routes_by_mode(mode)
    else:
        # If the user did not provide a preference, recommend routes based on time of day
        time = preferences.get('time')
        if time:
            routes = get_routes_by_time(time)
        else:
            routes = get_routes_by_time('morning')

# Get routes based on mode of transportation
def get_routes_by_mode(mode):
    routes = []
    if mode == 'walking':
        routes = ['Route 1', 'Route 3']
    elif mode == 'biking':
        routes = ['Route 2', 'Route 4']
    elif mode == 'driving':
        routes = ['Route 5', 'Route 6']
    return routes

# Get routes based on time of day
def get_routes_by_time(time):
    routes = []
    if time == 'morning':
        routes = ['Route 1', 'Route 2']
    elif time == 'afternoon':
        routes = ['Route 3', 'Route 4']
    elif time == 'evening':
        routes = ['Route 5', 'Route 6']
    return routes

# Load model for route recommendation
model = joblib.load('route_recommendation_model.pkl')

# Use the machine learning model to get route recommendations
def get_routes_recommendation(preferences):
    # Convert preferences to a format that the model can understand
    mode = 0 if preferences['mode'] == 'walking' else 1 if preferences['mode'] == 'biking' else 2
    time = 0 if preferences['time'] == 'morning' else 1 if preferences['time'] == 'afternoon' else 2
    input_data = [[mode, time]]

    # Get recommended routes from the model
    recommended_routes = model.predict(input_data)

    # Return the recommended routes
    return ['Route ' + str(i+1) for i in recommended_routes[0]]


# Get route recommendations based on user preferences   
@app.route('/routes', methods=['GET'])
def get_routes():
    """Get route recommendations based on user preferences."""
    # Get user preferences from request
    preferences = request.args
    print(preferences)
    # Implement route recommendation logic here
    # Get mode of transportation preference from request
    mode = preferences.get('mode')
    # If the user provided a preference for transportation mode
    if mode:
        # Recommend routes based on mode of transportation
        routes = get_routes_by_mode(mode)
    else:
        # If the user did not provide a preference, recommend routes based on time of day
        time = preferences.get('time')
        if time:
            routes = get_routes_by_time(time)
        else:
            routes = get_routes_by_time('morning')
    return jsonify({'routes': routes})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

