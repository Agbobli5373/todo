from pydantic import BaseModel, Field
import datetime


class TodoTask(BaseModel):
    id: int | None = Field(default=None)
    name: str
    is_overdue: bool = Field(default=False)
    is_completed: bool = Field(default=False)
    completed_at: datetime.datetime | None = Field(default=None)
    schedule_id: int | None = Field(default=None)


class TodoTaskSchedule(BaseModel):
    id: int
    name: str
    day_planned_to_complete: datetime.datetime
    repeat_every_x_days: int | None = Field(default=None)
    repeat_every_x_weeks: int | None = Field(default=None)
    repeat_every_x_months: int | None = Field(default=None)
