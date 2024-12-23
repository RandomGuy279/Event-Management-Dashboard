from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

class AttendeeModel(BaseModel):
    name: str = Field(..., description="Name of the attendee")
    phoneNumber: int = Field(..., description="Phone number of the attendee (10 digits)")
    email: Optional[EmailStr] = Field(None, description="Email address of the attendee (valid format)")

    @field_validator("phoneNumber")
    def validate_phone_number(cls, value):
        if len(str(value)) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value
