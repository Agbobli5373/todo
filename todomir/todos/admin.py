from django.contrib import admin

from todos.database.models import TodoTaskSchedule, TodoTask


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_day",
        "repeat_every_x_days",
        "repeat_every_x_weeks",
        "repeat_every_x_months",
    )

    def get_day(self, obj):
        return obj.day_planned_to_complete.strftime("%A")

    get_day.short_description = "day"


class TodoTaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_day",
    )

    def get_day(self, obj):
        return obj.day_planned_to_complete.strftime("%A")

    get_day.short_description = "day"


admin.site.register(TodoTaskSchedule, ScheduleAdmin)
admin.site.register(TodoTask, TodoTaskAdmin)
