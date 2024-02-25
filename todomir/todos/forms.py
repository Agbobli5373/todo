from django import forms
from django.core.exceptions import ValidationError

from todos.domain import repositories


class CompleteTaskForm(forms.Form):
    task_id = forms.IntegerField()

    def clean_task_id(self):
        task_id = self.cleaned_data["task_id"]
        repository = repositories.TodoTaskRepository()
        task = repository.get_by_id(task_id)

        if not task:
            raise ValidationError("Task does not exist!")

        if task.is_completed:
            raise ValidationError("Task was already completed!")

        return task.id


class NewTaskForm(forms.Form):
    new_task = forms.CharField(min_length=3, max_length=255)
