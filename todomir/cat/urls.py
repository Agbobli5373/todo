from django.urls import path
from cat import views

urlpatterns = [
    path("", views.cat_view, name="cat"),
]
