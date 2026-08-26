from pydantic import BaseModel, Field


class RejectBookingRequest(BaseModel):
    reason: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )


class BookingActionResponse(BaseModel):
    success: bool
    message: str
    booking_id: str