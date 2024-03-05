from pydantic import Field, field_serializer
from datetime import date
import humanize
import datetime
from common.domain import entities


class TodoTask(entities.DbEntity):
    name: str
    is_overdue: bool = Field(default=False)
    completed: datetime.datetime | None = Field(default=None)
    schedule_id: int | None = Field(default=None)
    external_id: str | None = Field(default=None)


class TodoTaskSchedule(entities.DbEntity):
    name: str
    day_planned_to_complete: date
    repeat_every_x_days: int | None = Field(default=None)
    repeat_every_x_weeks: int | None = Field(default=None)
    repeat_every_x_months: int | None = Field(default=None)

    @field_serializer("day_planned_to_complete")
    def serialize_dt(self, value: date, _info) -> str:
        return value.strftime("%Y-%m-%d")

    @property
    def day(self) -> str:
        return humanize.naturalday(self.day_planned_to_complete, format="%A, %b %d")

    @property
    def frequency_days(self) -> int:
        if self.repeat_every_x_days:
            return self.repeat_every_x_days
        if self.repeat_every_x_weeks:
            return self.repeat_every_x_weeks * 7

        # easy way to calculate but should be enough
        if self.repeat_every_x_months:
            return self.repeat_every_x_months * 7 * 4

        return 0

    @property
    def frequency(self) -> str | None:
        if self.repeat_every_x_days:
            return f"every {self.repeat_every_x_days} day(s)"

        if self.repeat_every_x_weeks:
            return f"every {self.repeat_every_x_weeks} week(s)"

        if self.repeat_every_x_months:
            return f"every {self.repeat_every_x_months} month(s)"

        return None
