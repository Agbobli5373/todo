from django.urls import path
from todos import views

urlpatterns = [
    path("", views.index, name="index"),
    path("schedules", views.schedules, name="schedules"),
    path("schedules/create", views.create_schedule, name="create_schedule"),
    path("schedules/<int:schedule_id>", views.edit_schedule, name="create_schedule"),
    # Actions
    path("complete", views.complete_task_view, name="complete"),
    path("add", views.add_new_task_view, name="add"),
]
