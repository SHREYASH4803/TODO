from flask import Flask
from pymongo import MongoClient
from config import Config
from routes.routes import create_todo_routes

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config["MONGO_URI"])
db = client.todo_db

app.register_blueprint(create_todo_routes(db))

# Vercel requires Flask apps to return WSGI-compatible app in function
def handler(request):
    return app(request)
