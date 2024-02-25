from django.urls import path
from todos import views

urlpatterns = [
    path("", views.index, name="index"),
    path("complete", views.complete_task_view, name="complete"),
    path("add", views.add_new_task_view, name="add"),
]
