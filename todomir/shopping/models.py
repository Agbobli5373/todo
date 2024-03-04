from django.db import models
from django.utils import timezone


class ShoppingListItem(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)

    class Meta:
        ordering = ("completed", "-created")
