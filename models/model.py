from bson.objectid import ObjectId


class TodoModel:
    def __init__(self, db):
        self.collection = db.todos

    def add_task(self, task_data):
        return self.collection.insert_one(task_data)

    def get_tasks(self):
        return list(self.collection.find())

    def update_task(self, task_id, updated_data):
        return self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})

    def delete_task(self, task_id):
        return self.collection.delete_one({"_id": ObjectId(task_id)})

    def delete_all_tasks(self):
        return self.collection.delete_many({})
