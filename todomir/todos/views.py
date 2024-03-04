from django.core.exceptions import ValidationError
from django.shortcuts import Http404, render
from todos import forms
from todos.domain import services

from django.views.decorators.http import require_POST, require_GET, require_http_methods


async def _get_tasks_context() -> dict:
    tasks = await services.get_tasks()
    return {
        "tasks": tasks,
        "all_completed": all(task.is_completed for task in tasks),
        "partially_completed": len([task for task in tasks if task.is_completed]),
    }


@require_GET
async def index(request):
    context = await _get_tasks_context()

    if request.htmx:
        return render(request, "partials/_index.html", context)

    return render(request, "index.html", context)


@require_GET
async def schedules(request):
    schedules = await services.get_schedules()
    if request.htmx:
        return render(request, "partials/_schedules.html", {"schedules": schedules})

    return render(request, "schedules.html", {"schedules": schedules})


@require_http_methods(["GET", "POST"])
async def create_schedule(request):
    context = {}
    form = forms.ScheduleForm()

    if request.method == "POST":
        form = forms.ScheduleForm(request.POST)
        if form.is_valid():
            schedule = await services.create_schedule(form.cleaned_data)
            schedules = await services.get_schedules()
            context = {
                "schedules": schedules,
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
async def edit_schedule(request, schedule_id: int):
    schedule = await services.get_schedule_by_id(schedule_id)
    if not schedule:
        raise Http404

    form = forms.ScheduleForm(schedule.model_dump())
    context = {"schedule": schedule, "form": form}

    if request.method == "POST":
        form = forms.ScheduleForm(request.POST)
        if form.is_valid():
            schedule = await services.update_schedule(schedule, form.cleaned_data)
            schedules = await services.get_schedules()
            context = {
                "schedules": schedules,
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
async def complete_task_view(request):
    form = forms.CompleteTaskForm(request.POST)
    if form.is_valid():
        task = await services.get_task_by_id(form.cleaned_data["task_id"])
        if not task:
            raise ValidationError("Task does not exist!")

        if task.is_completed:
            raise ValidationError("Task was already completed!")

        await services.complete_task(task.id)
    else:
        raise Exception("unhandled")

    context = await _get_tasks_context()
    if request.htmx:
        return render(request, "partials/_tasks.html", context)

    return render(request, "index.html", context)


@require_POST
async def add_new_task_view(request):
    form = forms.NewTaskForm(request.POST)
    if form.is_valid():
        await services.add_new_task(form.cleaned_data["new_task"])
    else:
        raise Exception("unhandled")

    context = await _get_tasks_context()
    if request.htmx:
        return render(request, "partials/_tasks.html", context)

    return render(request, "index.html", context)
