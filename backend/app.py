from flask import Flask, request, jsonify
from pymongo import MongoClient
from google.cloud import dialogflow_v2 as dialogflow
import os


# Initialize Flask app
app = Flask(__name__)

# Configure the database client and connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.chatbot_db

# Dialogflow setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'path_to_google_credentials.json'
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = 'your_project_id_here'

def detect_intent_texts(text, session_id, language_code='en'):
    """Detect intent with text input using Dialogflow."""
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

@app.route('/message', methods=['POST'])
def handle_message():
    """Handle incoming messages and respond with Dialogflow intent."""
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
    # Implement route recommendation logic here
    # For now, we'll send a placeholder response
    return jsonify({'routes': ['Route 1', 'Route 2', 'Route 3']})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
