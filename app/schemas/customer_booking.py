from pydantic import BaseModel
from typing import List, Any


class CustomerCreateBookingRequest(BaseModel):
    customer_name: str
    phone_number: str
    full_address: str

    latitude: float | None = None
    longitude: float | None = None

    services: List[Any]

    booking_date: str
    booking_time: str

    total_amount: float

    coupon_code: str | None = None
    coupon_discount_percentage: float = 0
    coupon_discount_amount: float = 0


class CustomerBookingResponse(BaseModel):
    id: str
    payment_status: str
    message: str


class CustomerCancelBookingResponse(BaseModel):
    success: bool
    message: str