from src.lib.responses import success, error
import src.db.requests_crud as requests_repo
from src.utils.serializer import serialize_complete_request


def get_request(event, _):
    try:
        request_id = event.get("pathParameters", {}).get("request_id")

        request = requests_repo.get(request_id=request_id)

        if not request:
            return error("Request not found", 404)
        serialized_request = serialize_complete_request(request)
        print(serialized_request)
        return success({"request": serialized_request.model_dump()})
    except Exception as e:
        return error(str(e))
