from pydantic import BaseModel
from typing import Dict, List, Union
from .auth import TokenModel

class ApiResponse(BaseModel):
    status_code: int = 200
    status_msg: str = ""
    body: Union[Dict, List[Dict], dict] = {}

class AuthenticationFailureResponse(ApiResponse):
    status_code: int = 401
    status_msg: str = "Invalid credentials"

class TokenApiSuccessResponse(ApiResponse):
    body: TokenModel

class EventApiSuccessResponse(ApiResponse):
    pass

class AttendeeApiSuccessResponse(ApiResponse):
    pass

class TaskApiSuccessResponse(ApiResponse):
    pass