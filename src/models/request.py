from typing import Optional
from src.enums import RequestType


class Request():
    
    request_id: str
    request_type: RequestType
    title: str
    description: str
    due_date: Optional[str] = None
    
    dropoff_latitude: float
    dropoff_longitude: float
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    
    user_id: str
    created_at: str
    updated_at: str
    
    @property
    def pk(self):
        return f"REQUEST#{self.request_id}"
    
    @property
    def sk(self):
        return f"METADATA#{self.request_id}"