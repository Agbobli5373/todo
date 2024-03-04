from django.urls import path
from cat import views

urlpatterns = [
    path("", views.index, name="cat-index"),
]
