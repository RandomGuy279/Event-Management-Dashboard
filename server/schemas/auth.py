from pydantic import BaseModel

# Pydantic model for the token response
class TokenModel(BaseModel):
    access_token: str = ""
    token_type: str = "bearer"