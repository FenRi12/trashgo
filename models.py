class Order(BaseModel):
    order_id: int
    user_id: int
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    phone: str = ""
    house: str = ""
    entrance: str = ""
    apartment: str = ""
    floor: str = ""
    door_code: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    time_slot: str = ""
    bags: int = 0
    payment: str = ""
    courier_id: int = 0
    status: str = ""
    created_at: str = ""
