from django.db import models

from todos.database import managers


class TodoTaskSchedule(models.Model):
    name = models.CharField(max_length=255)
    day_planned_to_complete = models.DateField()
    repeat_every_x_days = models.IntegerField(null=True, blank=True)
    repeat_every_x_weeks = models.IntegerField(null=True, blank=True)
    repeat_every_x_months = models.IntegerField(null=True, blank=True)


class TodoTask(models.Model):
    name = models.CharField(max_length=255)
    completed = models.DateTimeField(null=True, blank=True)
    day_planned_to_complete = models.DateField()
    schedule = models.ForeignKey(
        TodoTaskSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )

    objects = managers.TodoTaskManager()
