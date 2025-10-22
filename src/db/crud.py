from typing import Optional, Any
from src.schemas.request import RequestType


def create_request(
    user_id: int,
    request: RequestType,
    db_connection: Optional[
        Any
    ] = None,  # TODO: if no connection provided, use a default one
):
    # If no connection was provided, create one
    # if db_connection is None:
    #     db_connection = get_db_connection()  # your helper to create a connection

    # Need to be able to persist both of tables: main + specific sub table together or revert them both with transaction
    pass
