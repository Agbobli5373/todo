from django.shortcuts import Http404, render
from todos import forms
from todos.domain import services

from django.views.decorators.http import require_POST, require_GET, require_http_methods


def _get_tasks_context() -> dict:
    tasks = services.get_tasks()
    return {
        "tasks": tasks,
        "all_completed": all(task.is_completed for task in tasks),
        "partially_completed": len([task for task in tasks if task.is_completed]),
    }


@require_GET
def index(request):
    context = _get_tasks_context()

    if request.htmx:
        return render(request, "partials/_index.html", context)

    return render(request, "index.html", context)


@require_GET
def schedules(request):
    schedules = services.get_schedules()
    if request.htmx:
        return render(request, "partials/_schedules.html", {"schedules": schedules})

    return render(request, "schedules.html", {"schedules": schedules})


@require_http_methods(["GET", "POST"])
def create_schedule(request):
    context = {}
    form = forms.ScheduleForm()

    if request.method == "POST":
        form = forms.ScheduleForm(request.POST)
        if form.is_valid():
            schedule = services.create_schedule(form.cleaned_data)
            context = {
                "schedules": services.get_schedules(),
                "schedule": schedule,
                "action": "created",
            }
            if request.htmx:
                return render(request, "partials/_schedules.html", context)

            return render(request, "schedules.html", context)

    context["form"] = form
    if request.htmx:
        return render(request, "partials/_create_schedule.html", context=context)

    return render(request, "create_schedule.html", context=context)


@require_http_methods(["GET", "POST"])
def edit_schedule(request, schedule_id: int):
    schedule = services.get_schedule_by_id(schedule_id)
    if not schedule:
        raise Http404

    form = forms.ScheduleForm(schedule.model_dump())
    context = {"schedule": schedule, "form": form}

    if request.method == "POST":
        form = forms.ScheduleForm(request.POST)
        if form.is_valid():
            schedule = services.update_schedule(schedule, form.cleaned_data)
            context = {
                "schedules": services.get_schedules(),
                "schedule": schedule,
                "action": "updated",
            }
            if request.htmx:
                return render(request, "partials/_schedules.html", context)

            return render(request, "schedules.html", context)

    if request.htmx:
        return render(request, "partials/_edit_schedule.html", context=context)

    return render(request, "edit_schedule.html", context=context)


@require_POST
def complete_task_view(request):
    form = forms.CompleteTaskForm(request.POST)
    if form.is_valid():
        services.complete_task(form.cleaned_data["task_id"])
    else:
        raise Exception("unhandled")

    context = _get_tasks_context()
    if request.htmx:
        return render(request, "partials/_tasks.html", context)

    return render(request, "index.html", context)


@require_POST
def add_new_task_view(request):
    form = forms.NewTaskForm(request.POST)
    if form.is_valid():
        services.add_new_task(form.cleaned_data["new_task"])
    else:
        raise Exception("unhandled")

    context = _get_tasks_context()
    if request.htmx:
        return render(request, "partials/_tasks.html", context)

    return render(request, "index.html", context)
