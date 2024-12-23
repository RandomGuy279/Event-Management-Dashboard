from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from bson import ObjectId

from schemas.attendee import AttendeeModel
from schemas.response import (
        ApiResponse, 
        AttendeeApiSuccessResponse, 
        AuthenticationFailureResponse
)
from helpers.auth import get_current_user
from helpers.db_setup import dbConn

attendee_router = APIRouter()

@attendee_router.post("/attendees", response_model=ApiResponse)
def add_attendee(attendee: AttendeeModel, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        
        dbConn.insertData("attendees", attendee.dict())  # Insert the data into the database

        # Success response with the attendee data
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=AttendeeApiSuccessResponse(
                status_code=status.HTTP_201_CREATED,
                status_msg="Attendee created successfully",
                body=attendee.dict()  # Include the attendee data in the response
            ).dict()  # Return the response model as a dictionary
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error adding attendee: {e}",
                body={}
            ).dict()
        )


@attendee_router.put("/attendees/{attendee_id}", response_model=ApiResponse)
def update_attendee(attendee_id: str, attendee: AttendeeModel, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Convert the attendee data to a dictionary
        attendee_data = attendee.dict()

        # Update attendee in the database using the attendee_id
        updated = dbConn.updateData("attendees", {"_id": ObjectId(attendee_id)}, attendee_data)

        if not updated:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="Attendee not found",
                    body={}
                ).dict()
            )

        # Success response with the updated attendee data
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AttendeeApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Attendee updated successfully",
                body=attendee_data
            ).dict()
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error updating attendee: {e}",
                body={}
            ).dict()
        )

@attendee_router.get("/attendees", response_model=ApiResponse)
def get_attendees(current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Fetch all attendees from the database
        attendees = dbConn.getData("attendees", query={})

        if not attendees:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="No attendees found",
                    body={}
                ).dict()
            )
        
        for attendee in attendees:
            attendee["_id"] = str(attendee["_id"])

        # Success response with the list of attendees
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AttendeeApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Attendees fetched successfully",
                body=attendees
            ).dict()
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error fetching attendees: {e}",
                body={}
            ).dict()
        )

@attendee_router.delete("/attendees/{attendee_id}", response_model=ApiResponse)
def delete_attendee(attendee_id: str, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Delete the attendee from the database using the attendee_id
        deleted = dbConn.deleteData("attendees", {"_id": ObjectId(attendee_id)})

        if not deleted:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="Attendee not found",
                    body={}
                ).dict()
            )

        # Success response indicating deletion
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ApiResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Attendee deleted successfully",
                body={}
            ).dict()
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error deleting attendee: {e}",
                body={}
            ).dict()
        )
