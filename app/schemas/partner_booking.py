from pydantic import BaseModel
from typing import Any


class PartnerBooking(BaseModel):
    id: str
    customer_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    services: Any | None = None
    booking_date: str | None = None
    booking_time: str | None = None
    work_status: str | None = None
    staff_response: str | None = None
    total_staff_amount: float | None = None
    staff_earned_amount: float | None = None
    work_started_at: str | None = None
    work_ended_at: str | None = None