import datetime
import django.utils.timezone
from django.shortcuts import render
from .forms import Task
from .models import TaskBase
import time
from django.shortcuts import redirect


PRIORITY_CHOICES = {
    "1": "Низкий",
    "2": "Средний",
    "3": "Высокий",
}


def index(request):
    return render(request, "app1/start_page.html")


def create_task(request):
    if request.method == "POST":
        summary = request.POST.get("summary")
        priority_id = request.POST.get("priority")
        priority_name = PRIORITY_CHOICES[priority_id]
        description = request.POST.get("description")
        due_date = (time.strftime("%d-%m-%Y %H:%M", time.strptime(request.POST.get("due_date"), "%Y-%m-%dT%H:%M")))
        created_date = django.utils.timezone.now().strftime("%d-%m-%Y %H:%M")

        task = TaskBase(summary, priority_name, description, due_date, created_date)
        task_id = TaskBase.save_task(task)
        return redirect("create_success", task_id=task_id)
    else:
        new_task = Task()
        return render(request, "app1/create_task.html", {"form": new_task})


def view_tasks(request):
    tasks_json = TaskBase.get_data()
    if tasks_json:
        return render(request, "app1/view_tasks.html", {"my_tasks": tasks_json["task_list"]})
    return render(request, "app1/error.html")


def detail_task(request, task_id):
    if request.method == "POST":
        action_type = request.POST.get('action')
        if action_type == "Сохранить":
            summary = request.POST.get("summary")
            priority_id = request.POST.get("priority")
            priority_name = PRIORITY_CHOICES[priority_id]
            description = request.POST.get("description")
            due_date = (time.strftime("%d-%m-%Y %H:%M", time.strptime(request.POST.get("due_date"), "%Y-%m-%dT%H:%M")))

            updated_data = {
                "summary": summary,
                "priority": priority_name,
                "description": description,
                "due_date": due_date,
            }

            TaskBase.update_task(task_id, updated_data)
            return redirect("edit_success", task_id=task_id)

        elif action_type == "Удалить":
            TaskBase.delete_task(task_id)
            return redirect("delete_success", task_id=task_id)
    else:
        try:
            task = TaskBase.get_task_data(task_id)
            if task != "Task not Found":
                form = Task(initial={
                    'summary': task["summary"],
                    'priority': task["priority"],
                    'description': task['description'],
                    'due_date': datetime.datetime.strptime(task["due_date"], "%d-%m-%Y %H:%M"),
                })
                return render(request, "app1/detail_task.html", {"form": form, "task_id": task_id})
            else:
                return render(request, "app1/error.html")
        except TypeError:
            return render(request, "app1/error.html")


def create_success(request, task_id):
    return render(request, "app1/create_success.html", {"task_id": task_id})


def edit_success(request, task_id):
    return render(request, "app1/edit_success.html", {"task_id": task_id})


def delete_success(request, task_id):
    return render(request, "app1/delete_success.html", {"task_id": task_id})


def error(request):
    return render(request, "app1/error.html")