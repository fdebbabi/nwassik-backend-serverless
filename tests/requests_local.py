import json
from uuid import uuid4
from src.handlers.requests.create import create_request

# Example body for a buy_and_deliver request
body = {
    "request_type": "online_service",
    "title": "Buy netflix",
    "description": "Need a package delivered from France",
    "meetup_latitude": 36.8,
    "meetup_longitude": 10.2,
    "due_date": "2025-10-29T12:34:56Z",
}

# Mock Lambda event
event = {
    "body": json.dumps(body),
    "requestContext": {
        "authorizer": {
            "claims": {
                "sub": str(uuid4())  # user_id for testing
            }
        }
    },
}

print(event["requestContext"]["authorizer"]["claims"]["sub"])
# Context can be None for local testing
response = create_request(event, None)
print(response)
