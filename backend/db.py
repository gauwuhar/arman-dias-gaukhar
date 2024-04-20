from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.chatbot  # 'chatbot' is the name of the database

def save_message(user_id, message):
    messages = db.messages  # 'messages' is a collection
    messages.insert_one({"user_id": user_id, "message": message})
