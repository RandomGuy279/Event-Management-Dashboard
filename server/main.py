from fastapi import FastAPI, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from helpers.config import configData
from helpers.logger_setup import logger
from helpers.user_setup import addDefaultUser
from helpers.auth import get_current_user
from api.token import token_router
from api.event import event_router
from api.attendee import attendee_router
from api.task import task_router

addDefaultUser()

app = FastAPI()
app.include_router(token_router, tags=["Authentication"])
app.include_router(event_router, tags=["Events"])
app.include_router(attendee_router, tags=["Attendees"])
app.include_router(task_router, tags=["Tasks"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a test API response", "user": current_user}


uvicorn.run(app, 
            host=configData["server"]["host"], 
            port=configData["server"]["port"],
            log_config=configData.get("logConfiguration")
            )
