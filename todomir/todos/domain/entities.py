from pydantic import BaseModel, Field, field_serializer
from datetime import date
import humanize
import datetime


class TodoTask(BaseModel):
    id: int | None = Field(default=None)
    name: str
    is_overdue: bool = Field(default=False)
    is_completed: bool = Field(default=False)
    completed_at: datetime.datetime | None = Field(default=None)
    schedule_id: int | None = Field(default=None)
    external_id: str | None = Field(default=None)


class TodoTaskSchedule(BaseModel):
    id: int | None = Field(default=None)
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
    def frequency(self) -> str | None:
        if self.repeat_every_x_days:
            return f"every {self.repeat_every_x_days} day(s)"

        if self.repeat_every_x_weeks:
            return f"every {self.repeat_every_x_weeks} week(s)"

        if self.repeat_every_x_months:
            return f"every {self.repeat_every_x_months} month(s)"

        return None
