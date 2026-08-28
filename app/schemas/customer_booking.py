from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class CustomerBookingCreateRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=150)
    email: str = Field(..., min_length=3, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=15)

    full_address: str = Field(
        ...,
        min_length=1,
        max_length=1000,
    )

    services: Any

    booking_date: date
    booking_time: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    total_amount: float = Field(
        ...,
        gt=0,
    )


class CustomerBookingResponse(BaseModel):
    success: bool
    booking_id: str
    message: str
    payment_status: str
    payment_verified: bool