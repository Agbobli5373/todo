from django.urls import path
from todos import views

urlpatterns = [
    path("", views.index, name="todos-index"),
    path("todos/complete", views.complete_task, name="todos-complete-task"),
    path("todos/undo", views.undo_task, name="todos-undo-task"),
    path("todos/create", views.create_new_task, name="todos-create-task"),
    path("schedules", views.schedules, name="todos-schedules"),
    path("schedules/create", views.create_schedule, name="todos-create-schedule"),
    path(
        "schedules/<int:schedule_id>",
        views.edit_schedule,
        name="todos-schedule-details",
    ),
]
