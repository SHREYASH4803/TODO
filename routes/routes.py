from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.model import TodoModel

todo_routes = Blueprint("todo_routes", __name__)

def create_todo_routes(db):
    todo_model = TodoModel(db)

    @todo_routes.route("/")
    def home():
        tasks = todo_model.get_tasks()
        for task in tasks:
            task["_id"] = str(task["_id"])
        return render_template("index.html", tasks=tasks)

    @todo_routes.route("/todos", methods=["POST"])
    def add_task():
        data = request.form
        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400
        task = {"title": data["title"], "description": data.get("description", ""), "status": "Pending"}
        todo_model.add_task(task)
        return redirect(url_for("todo_routes.home"))

    @todo_routes.route("/todos/<task_id>/edit", methods=["POST"])
    def edit_task(task_id):
        updated_data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
        }
        todo_model.update_task(task_id, updated_data)
        return redirect(url_for("todo_routes.home"))

    @todo_routes.route("/todos/<task_id>/delete", methods=["POST"])
    def delete_task(task_id):
        todo_model.delete_task(task_id)
        return redirect(url_for("todo_routes.home"))

    @todo_routes.route("/todos/delete_all", methods=["POST"])
    def delete_all_tasks():
        todo_model.delete_all_tasks()
        return redirect(url_for("todo_routes.home"))

    return todo_routes
