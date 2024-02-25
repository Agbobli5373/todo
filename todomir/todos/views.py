from django.shortcuts import render
from todos import forms
from todos.domain import services

from django.views.decorators.http import require_POST, require_GET


def render_tasks(request):
    tasks = services.get_tasks()
    context = {
        "tasks": tasks,
        "all_completed": all(task.is_completed for task in tasks),
        "partially_completed": len([task for task in tasks if task.is_completed]),
    }

    if request.htmx:
        return render(request, "partials/tasks.html", context)
    return render(request, "index.html", context)


@require_GET
def index(request):
    return render_tasks(request)


@require_POST
def complete_task_view(request):
    form = forms.CompleteTaskForm(request.POST)
    if form.is_valid():
        services.complete_task(form.cleaned_data["task_id"])
    else:
        raise Exception("unhandled")

    return render_tasks(request)


@require_POST
def add_new_task_view(request):
    form = forms.NewTaskForm(request.POST)
    if form.is_valid():
        services.add_new_task(form.cleaned_data["new_task"])
    else:
        raise Exception("unhandled")
    return render_tasks(request)
