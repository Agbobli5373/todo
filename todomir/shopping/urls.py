from django.urls import path
from shopping import views

urlpatterns = [
    path("", views.index, name="shopping-list-index"),
    path("create", views.create_new_item, name="shopping-list-create-item"),
    path("complete", views.complete_item, name="shopping-list-complete-item"),
    path("undo", views.undo_item, name="shopping-list-undo-item"),
]
