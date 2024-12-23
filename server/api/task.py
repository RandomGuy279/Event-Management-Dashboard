from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import Literal


from helpers.logger_setup import logger
from schemas.task import TaskModel
from schemas.response import (
        ApiResponse, 
        TaskApiSuccessResponse, 
        AuthenticationFailureResponse
)
from helpers.auth import get_current_user
from helpers.db_setup import dbConn

task_router = APIRouter()


@task_router.post("/tasks", response_model=ApiResponse)
def create_task(task: TaskModel, event_id: str, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Insert the task into the database with the event ID
        task_data = task.dict()
        task_data["event_id"] = ObjectId(event_id)  # Attach the event_id to the task

        dbConn.insertData("tasks", task_data)

        # Success response with the task data
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=TaskApiSuccessResponse(
                status_code=status.HTTP_201_CREATED,
                status_msg="Task created successfully",
                body=task.dict()
            ).dict()  # Return the response model as a dictionary
        )

    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error creating task: {e}",
                body={}
            ).dict()
        )

@task_router.get("/tasks", response_model=ApiResponse)
def get_tasks(event_id: str = None, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # If event_id is provided, fetch tasks for that event
        if event_id:
            tasks = dbConn.getData("tasks", query={"event_id": ObjectId(event_id)})
        else:
            # If no event_id is provided, fetch tasks for all events
            tasks = dbConn.getData("tasks", query={})

        if not tasks:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="No tasks found",
                    body={}
                ).dict()
            )

        for task in tasks:
            task['event_id'] = str(task['event_id'])
            task['_id'] = str(task['_id'])

        # Success response with the list of tasks
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=TaskApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Tasks fetched successfully",
                body=tasks
            ).dict()
        )

    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error fetching tasks: {e}",
                body={}
            ).dict()
        )


@task_router.put("/tasks/{task_id}", response_model=ApiResponse)
def update_task_status(task_id: str, status: Literal["Pending", "Completed"], current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Update the status of the task in the database
        updated = dbConn.updateData("tasks", {"_id": ObjectId(task_id)}, {"status": status})

        if not updated:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="Task not found",
                    body={}
                ).dict()
            )

        # Success response with the updated task status
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=TaskApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Task status updated successfully",
                body={"task_id": task_id, "status": status}
            ).dict()
        )

    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error updating task status: {e}",
                body={}
            ).dict()
        )
