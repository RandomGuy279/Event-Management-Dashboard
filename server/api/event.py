from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from bson import ObjectId


from schemas.event import Event
from schemas.response import (
        ApiResponse, 
        EventApiSuccessResponse, 
        AuthenticationFailureResponse
)
from helpers.auth import get_current_user
from helpers.db_setup import dbConn

event_router = APIRouter()

@event_router.post("/events", response_model=ApiResponse)
def add_event(event: Event, current_user: dict = Depends(get_current_user)):
    try:
        if not current_user:
            return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=AuthenticationFailureResponse().dict() 
        )
        # Insert event data into the database
        dbConn.insertData("events", event.dict())  
        
        # Success response with the event data
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=EventApiSuccessResponse(
                status_code=status.HTTP_201_CREATED,
                status_msg="Event created successfully",
                body=event.dict()  
            ).dict()  
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error adding event: {e}",
                body={}
            ).dict()
        )
    
@event_router.put("/events/{event_id}", response_model=ApiResponse)
def update_event(event_id: str, event: Event, current_user: dict = Depends(get_current_user)):
    try:
        # Check if the user is authenticated
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict() 
            )

        # Check if the event exists in the database
        existing_event = dbConn.getData("events", query={"_id": ObjectId(event_id)})
        if not existing_event:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="Event not found",
                    body={}
                ).dict()
            )

        
        updated_event_data = event.dict()

        dbConn.updateData("events", query={"_id": ObjectId(event_id)}, data=updated_event_data)

    
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=EventApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Event updated successfully",
                body=updated_event_data  
            ).dict()
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error updating event: {e}",
                body={}
            ).dict()
        )

@event_router.get("/events", response_model=ApiResponse)
def get_all_events(current_user: dict = Depends(get_current_user)):
    try:
        # Check if the user is authenticated
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )

        # Get all events from the database
        events = dbConn.getData("events")

        # If no events found, return a not found response
        if not events:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="No events found",
                    body={}
                ).dict()
            )
        
        for event in events:
            event["_id"] = str(event["_id"])

        # Success response with the list of events
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=EventApiSuccessResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Events retrieved successfully",
                body=events  # Returning the list of events
            ).dict()
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error retrieving events: {e}",
                body={}
            ).dict()
        )

@event_router.delete("/events/{event_id}", response_model=ApiResponse)
def delete_event(event_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # Check if the user is authenticated
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=AuthenticationFailureResponse().dict()  # Return authentication failure response
            )
        
        # Find the event by its ID
        event = dbConn.getData("events", query={"_id": ObjectId(event_id)})

        # If the event is not found, return a 404 not found response
        if not event:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ApiResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    status_msg="Event not found",
                    body={}
                ).dict()
            )
        
        # Proceed with deletion
        dbConn.deleteData("events", query={"_id": ObjectId(event_id)})

        # Return a success response after deleting the event
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ApiResponse(
                status_code=status.HTTP_200_OK,
                status_msg="Event deleted successfully",
                body={}
            ).dict()
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_msg=f"Error deleting event: {e}",
                body={}
            ).dict()
        )
