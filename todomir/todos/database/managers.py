from datetime import date
from django.db.models import Case, When, BooleanField, Value
from django.db import models


class TodoTaskManager(models.Manager):
    def get_queryset(self):
        today = date.today()
        return (
            super()
            .get_queryset()
            .annotate(
                is_overdue=Case(
                    When(day_planned_to_complete__lt=today, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        )
