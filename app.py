from flask import Flask
from pymongo import MongoClient
from config import Config
from routes.routes import create_todo_routes

app = Flask(__name__)
app.config.from_object(Config)

# Connect to MongoDB
client = MongoClient(app.config["MONGO_URI"])
db = client.todo_db

# Register the Blueprint for To-Do routes
app.register_blueprint(create_todo_routes(db))

# Run the app only when running locally (not needed on PythonAnywhere)
if __name__ == "__main__":
    app.run()
