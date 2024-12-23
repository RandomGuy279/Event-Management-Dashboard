from pydantic import BaseModel, Field, field_validator
from typing import List
import time

class Event(BaseModel):
    """Model to represent an event."""
    name: str = Field(..., description="Name of the event")
    description: str = Field(..., description="Description of the event")
    location: str = Field(..., description="Location of the event")
    date: int = Field(..., description="Phone number of the attendee (10 digits)")
    attendees: List = Field(default_factory=list, description="List of attendees for the event")

    @field_validator("name", "location")
    def validate_non_empty_fields(cls, value):
        if not value.strip():
            raise ValueError("Name and location must not be empty")
        return value

    @field_validator("date")
    def validate_date(cls, value):
        if value < int(time.time()):
            raise ValueError("Event date cannot be in the past")
        return value
