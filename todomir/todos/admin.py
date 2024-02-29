from django.contrib import admin
import humanize

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
        return humanize.naturalday(obj.day_planned_to_complete, format="%A, %b %d")

    get_day.short_description = "day"

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("day_planned_to_complete")


class TodoTaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_day",
    )

    def get_day(self, obj):
        return humanize.naturalday(obj.day_planned_to_complete, format="%A, %b %d")

    get_day.short_description = "day"


admin.site.register(TodoTaskSchedule, ScheduleAdmin)
admin.site.register(TodoTask, TodoTaskAdmin)
