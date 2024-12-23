from fastapi import APIRouter, Form, status
from fastapi.responses import JSONResponse

from schemas.auth import TokenModel
from schemas.response import (
    ApiResponse,
    TokenApiSuccessResponse,
    AuthenticationFailureResponse
)
from helpers.auth import create_access_token
from helpers.db_setup import dbConn


token_router = APIRouter()

# Endpoint to generate JWT token after login
@token_router.post("/token", response_model=ApiResponse)
def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    
    user = dbConn.getData("users", query={"username": username})

    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content=AuthenticationFailureResponse().dict()  
        )
    
    if password != user[0]["password"]:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content=AuthenticationFailureResponse().dict()
        )

    
    access_token = create_access_token(data={"sub": username})


    return JSONResponse(
        status_code=status.HTTP_200_OK,  
        content=TokenModel(
                access_token=access_token,
                token_type="bearer"
            
        ).dict()  
    )