from pydantic import BaseModel, Field, field_validator
from typing import Literal, List
import time

class TaskModel(BaseModel):
    """Model to represent a task."""
    name: str = Field(..., description="Name of the task")
    deadline: int = Field(..., description="Deadline for the task")
    status: Literal["Pending", "Completed"] = Field("Pending", description="Status of the task")
    attendees: List = Field(default_factory=list, description="List of attendees for the task")

    @field_validator("deadline")
    def validate_deadline(cls, v):
        if v < int(time.time()):
            raise ValueError("Deadline must be in the future.")
        return v
