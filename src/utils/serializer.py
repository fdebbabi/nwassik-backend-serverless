from src.models.request import Request
from src.schemas.request import (
    CompleteRequest,
    RequestType,
    BuyAndDeliverRequest,
    PickupAndDeliverRequest,
    OnlineServiceRequest,
)


def serialize_complete_request(db_request: Request) -> CompleteRequest:
    """Convert SQLAlchemy Request object to appropriate Pydantic model"""

    # Convert to dict first
    request_dict = {
        "id": db_request.id,
        "user_id": db_request.user_id,
        "type": db_request.type,
        "title": db_request.title,
        "description": db_request.description,
        "due_date": db_request.due_date,
        "created_at": db_request.created_at,
    }

    # Add specific fields based on request type
    if db_request.type == RequestType.BUY_AND_DELIVER:
        request_dict.update(
            {
                "dropoff_latitude": db_request.buy_and_deliver.dropoff_latitude,
                "dropoff_longitude": db_request.buy_and_deliver.dropoff_longitude,
            }
        )
        return BuyAndDeliverRequest.model_validate(request_dict)

    elif db_request.type == RequestType.PICKUP_AND_DELIVER:
        request_dict.update(
            {
                "pickup_latitude": db_request.pickup_and_deliver.pickup_latitude,
                "pickup_longitude": db_request.pickup_and_deliver.pickup_longitude,
                "dropoff_latitude": db_request.pickup_and_deliver.dropoff_latitude,
                "dropoff_longitude": db_request.pickup_and_deliver.dropoff_longitude,
            }
        )
        return PickupAndDeliverRequest.model_validate(request_dict)

    elif db_request.type == RequestType.ONLINE_SERVICE:
        request_dict.update(
            {
                "meetup_latitude": db_request.online_service.meetup_latitude,
                "meetup_longitude": db_request.online_service.meetup_longitude,
            }
        )
        return OnlineServiceRequest.model_validate(request_dict)

    else:
        # FIXME: This is not clean..
        raise ValueError("No request type matched in from types in RequestType")
