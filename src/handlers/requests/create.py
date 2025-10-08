import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import sys
import os

from src.lib.responses import success, error
from src.schemas.request import RequestCreate
from src.enums import RequestType
from src.lib.database import get_dynamodb_table_connexion

def create_request(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        # NOTE: Validation could have been outside of Lambda and at API Gateway level, 
        # for faster error response and no Lambda execution on schema validation failure, 
        # but I need dynamic cross-attributes check which is not possible in API Gateway. 
        # Only static stuff is supported for now in API Gateway
        request_data = RequestCreate.model_validate(**body) 
        
        claims = event.get("requestContext").get("authorizer").get("claims")
        user_id = claims.get("sub")
        db = get_dynamodb_table_connexion()
        request_id = str(uuid.uuid4())
        
        # ISO string or fallback for GSI sort key
        due_date_str = request_data.due_date.isoformat() if request_data.due_date else "0000-00-00T00:00:00Z" # FIXME: bad date


        request = {
            "gsi_pk": f"USER#{user_id}",                     # GSI HASH
            "gsi_sk": due_date_str,                          # GSI RANGE


            'request_id': request_id,
            'request_type': request_data.request_type,
            'title': request_data.title,
            'description': request_data.description,
            'due_date': request_data.due_date.isoformat() if request_data.due_date else None,

            'dropoff_latitude': Decimal(str(request_data.dropoff_latitude)),
            'dropoff_longitude': Decimal(str(request_data.dropoff_longitude)),
            'pickup_latitude': Decimal(str(request_data.pickup_latitude)), # FIXME: error will be raised in case no pickup as request_data.pickup_latitude will be None
            'pickup_longitude': Decimal(str(request_data.pickup_longitude)), # FIXME: Same issue


            'user_id': user_id,
            
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        db.put_item(Item=request)


        return success({
            "message": "Request created successfully",
            "request_id": request_id,
        })
    except Exception as e:
        return error(str(e))