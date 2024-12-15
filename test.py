import pytest
from app import app
from pymongo import MongoClient


TEST_MONGO_URI = "mongodb+srv://shreyash4803:shreyash4803@todoapp.jxs7g.mongodb.net/?retryWrites=true&w=majority&appName=TODOAPP"
client = MongoClient(TEST_MONGO_URI)
db = client.todo_db
todos_collection = db.todos

@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = TEST_MONGO_URI
    with app.test_client() as client:
        yield client
   
    todos_collection.delete_many({})


def print_test_result(test_name, status):
    """Helper function to print test result."""
    print(f"Test '{test_name}' {status}")


def test_add_task(test_client):
    """Test adding a new task."""
    response = test_client.post("/todos", data={"title": "Test Task", "description": "Test Description"})
    if response.status_code == 302:
        print_test_result('test_add_task', 'PASSED')
    else:
        print_test_result('test_add_task', 'FAILED')
    tasks = list(todos_collection.find({"title": "Test Task"}))
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test Description"


def test_display_tasks(test_client):
    """Test retrieving the task list."""
    todos_collection.insert_one({"title": "Task 1", "description": "Desc 1", "status": "Pending"})
    todos_collection.insert_one({"title": "Task 2", "description": "Desc 2", "status": "Pending"})
    response = test_client.get("/")
    if response.status_code == 200:
        print_test_result('test_display_tasks', 'PASSED')
    else:
        print_test_result('test_display_tasks', 'FAILED')
    assert response.status_code == 200
    assert b"Task 1" in response.data
    assert b"Task 2" in response.data


def test_edit_task(test_client):
    """Test editing an existing task."""
    task = todos_collection.insert_one({"title": "Old Task", "description": "Old Desc", "status": "Pending"})
    task_id = str(task.inserted_id)
    response = test_client.post(f"/todos/{task_id}/edit", data={"title": "Updated Task", "description": "Updated Desc"})
    if response.status_code == 302:
        print_test_result('test_edit_task', 'PASSED')
    else:
        print_test_result('test_edit_task', 'FAILED')
    updated_task = todos_collection.find_one({"_id": task.inserted_id})
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated Desc"


def test_delete_task(test_client):
    """Test deleting a specific task."""
    task = todos_collection.insert_one({"title": "Task to Delete", "description": "Delete Desc", "status": "Pending"})
    task_id = str(task.inserted_id)
    response = test_client.post(f"/todos/{task_id}/delete")
    if response.status_code == 302:
        print_test_result('test_delete_task', 'PASSED')
    else:
        print_test_result('test_delete_task', 'FAILED')
    deleted_task = todos_collection.find_one({"_id": task.inserted_id})
    assert deleted_task is None


def test_delete_all_tasks(test_client):
    """Test deleting all tasks."""
    todos_collection.insert_one({"title": "Task 1", "description": "Desc 1", "status": "Pending"})
    todos_collection.insert_one({"title": "Task 2", "description": "Desc 2", "status": "Pending"})
    response = test_client.post("/todos/delete_all")
    if response.status_code == 302:
        print_test_result('test_delete_all_tasks', 'PASSED')
    else:
        print_test_result('test_delete_all_tasks', 'FAILED')
    remaining_tasks = list(todos_collection.find({}))
    assert len(remaining_tasks) == 0
