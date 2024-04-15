import json
import os
from project1.settings import BASE_DIR

# Create your models here.
FILE_PATH = os.path.join(BASE_DIR, 'app1/tasks_storage.json')


class TaskBase:
    def __init__(self, summary, priority, description, due_date, created_date):
        self.summary = summary
        self.priority = priority
        self.description = description
        self.due_date = due_date
        self.created_date = created_date

    def save_task(self):
        if not os.path.exists(FILE_PATH):
            data = {
                "task_counter": 0,
                "task_list": {}
            }
            with open(FILE_PATH, mode='w') as f:
                json.dump(data, f, indent=4)

        with open(FILE_PATH, mode="r+", encoding="utf-8") as f:
            data = json.load(f)
            data["task_counter"] += 1
            data["task_list"][data["task_counter"]] = {
                'summary': self.summary,
                'priority': self.priority,
                'description': self.description,
                'due_date': self.due_date,
                'created_date': self.created_date,
            }
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            return data["task_counter"]

    @classmethod
    def get_data(cls):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, mode="r", encoding="utf-8") as f:
                data = json.load(f)
            return data

    @classmethod
    def get_task_data(cls, task_id):
        try:
            data = TaskBase.get_data()["task_list"][task_id]
        except:
            return "Task not Found!"
        return data

    @classmethod
    def update_task(cls, task_id, updated_data):
        data = cls.get_data()
        updated_data["created_date"] = data["task_list"][task_id]["created_date"]
        data["task_list"][task_id] = updated_data

        with open(FILE_PATH, mode="w", encoding="utf-8") as f:
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def delete_task(cls, task_id):
        data = cls.get_data()
        del data["task_list"][task_id]
        with open(FILE_PATH, mode="w", encoding="utf-8") as f:
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
