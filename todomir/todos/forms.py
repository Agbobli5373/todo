from django import forms
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class TaskIDForm(forms.Form):
    task_id = forms.IntegerField()


class NewTaskForm(forms.Form):
    new_task = forms.CharField(min_length=3, max_length=255)


class ScheduleForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=255)
    day_planned_to_complete = forms.DateField()
    repeat_every_x_days = forms.IntegerField(required=False)
    repeat_every_x_weeks = forms.IntegerField(required=False)
    repeat_every_x_months = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["day_planned_to_complete"].initial = date.today() + timedelta(
            days=1
        )

    def clean_day_planned_to_complete(self):
        day = self.cleaned_data["day_planned_to_complete"]
        if day <= date.today():
            raise ValidationError("This must be a future date")

        return day

    def clean(self):
        cleaned_data = super().clean()

        frequency_values = [
            cleaned_data["repeat_every_x_days"],
            cleaned_data["repeat_every_x_weeks"],
            cleaned_data["repeat_every_x_months"],
        ]
        if len(list(filter(lambda x: x, map(bool, frequency_values)))) > 1:
            msg = "Only one of these fields should be set"
            self.add_error("repeat_every_x_days", msg)
            self.add_error("repeat_every_x_weeks", msg)
            self.add_error("repeat_every_x_months", msg)

        return cleaned_data
