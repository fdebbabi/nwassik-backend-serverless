from typing import TYPE_CHECKING

from src.db.session import get_db_session
from src.models.request import (
    Request,
    BuyAndDeliverRequest,
    PickupAndDeliverRequest,
    OnlineServiceRequest,
)

if TYPE_CHECKING:
    from src.schemas.request import RequestCreate
    from uuid import UUID


def insert_request(user_id: "UUID", request: "RequestCreate"):
    with get_db_session() as db:
        main_request = Request(
            user_id=user_id,
            request_type=request.request_type,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )
        db.add(main_request)
        db.flush()  # main_request.id available

        # Create subtype
        if request.request_type.name == "buy_and_deliver":
            db.add(
                BuyAndDeliverRequest(
                    request_id=main_request.id,
                    dropoff_latitude=request.dropoff_latitude,
                    dropoff_longitude=request.dropoff_longitude,
                )
            )
        elif request.request_type.name == "pickup_and_deliver":
            db.add(
                PickupAndDeliverRequest(
                    request_id=main_request.id,
                    pickup_latitude=request.pickup_latitude,
                    pickup_longitude=request.pickup_longitude,
                    dropoff_latitude=request.dropoff_latitude,
                    dropoff_longitude=request.dropoff_longitude,
                )
            )
        else:  # online_service
            db.add(
                OnlineServiceRequest(
                    request_id=main_request.id,
                    meetup_latitude=request.meetup_latitude,
                    meetup_longitude=request.meetup_longitude,
                )
            )
        # Mandatory to have up to date fields
        db.refresh(main_request)

        # NOTE: we are still inside of a context manager block
        # So still no commit. The commit happends automatically
        # in the wrapper
        return main_request


# -------------------------------
# Read
# -------------------------------
def get_request(request_id):
    with get_db_session() as db:
        return db.query(Request).filter(Request.id == request_id).first()


def get_requests_batch(limit=30, offset=0):
    with get_db_session() as db:
        return (
            db.query(Request)
            .order_by(Request.due_date)
            .offset(offset)
            .limit(limit)
            .all()
        )


# -------------------------------
# Update
# -------------------------------
def update_request(request_id, data: dict):
    with get_db_session() as db:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            return None
        for k, v in data.items():
            setattr(req, k, v)
        db.commit()
        db.refresh(req)
        return req


# -------------------------------
# Delete
# -------------------------------
def delete_request(request_id):
    with get_db_session() as db:
        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            return False
        db.delete(req)
        db.commit()
        return True
