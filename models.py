from typing import Optional
from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    house: Optional[str] = None
    entrance: Optional[str] = None
    apartment: Optional[str] = None
    floor: Optional[str] = None
    door_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    time_slot: Optional[str] = None
    bags: Optional[int] = None
    payment: Optional[str] = None
    courier_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
