# from datetime import date
# from typing import Any

# from pydantic import BaseModel, Field


# class CustomerBookingCreateRequest(BaseModel):
#     customer_name: str = Field(..., min_length=1, max_length=150)
#     email: str = Field(..., min_length=3, max_length=255)
#     phone_number: str = Field(..., min_length=10, max_length=15)

#     full_address: str = Field(
#         ...,
#         min_length=1,
#         max_length=1000,
#     )

#     services: Any

#     booking_date: date
#     booking_time: str = Field(
#         ...,
#         min_length=1,
#         max_length=50,
#     )

#     total_amount: float = Field(
#         ...,
#         gt=0,
#     )


# class CustomerBookingResponse(BaseModel):
#     success: bool
#     booking_id: str
#     message: str
#     payment_status: str
#     payment_verified: bool












# from datetime import date
# from typing import Any

# from pydantic import BaseModel, Field, EmailStr


# class CustomerBookingCreateRequest(BaseModel):
#     customer_name: str = Field(
#         ...,
#         min_length=1,
#         max_length=150,
#     )

#     email: EmailStr

#     phone_number: str = Field(
#         ...,
#         min_length=10,
#         max_length=15,
#     )

#     full_address: str = Field(
#         ...,
#         min_length=1,
#         max_length=1000,
#     )

#     # Example:
#     # [
#     #   {
#     #     "id": "service-uuid",
#     #     "quantity": 1
#     #   }
#     # ]
#     services: list[dict[str, Any]] = Field(
#         ...,
#         min_length=1,
#     )

#     # Example:
#     # [
#     #   {
#     #     "id": "addon-uuid",
#     #     "quantity": 2
#     #   }
#     # ]
#     add_ons: list[dict[str, Any]] = Field(
#         default_factory=list,
#     )

#     booking_date: date

#     booking_time: str = Field(
#         ...,
#         min_length=1,
#         max_length=50,
#     )

#     latitude: float | None = None
#     longitude: float | None = None

#     location_link: str | None = Field(
#         default=None,
#         max_length=2000,
#     )


# class CustomerBookingResponse(BaseModel):
#     success: bool
#     booking_id: str
#     message: str
#     payment_status: str
#     payment_verified: bool
#     total_amount: float
















from datetime import date
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class CustomerBookingCreateRequest(BaseModel):
    customer_name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    email: EmailStr

    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

    full_address: str = Field(
        ...,
        min_length=1,
        max_length=1000,
    )

    services: list[dict[str, Any]] = Field(
        ...,
        min_length=1,
    )

    add_ons: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    booking_date: date

    booking_time: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    latitude: float | None = None

    longitude: float | None = None

    location_link: str | None = Field(
        default=None,
        max_length=2000,
    )


class CustomerBookingResponse(BaseModel):
    success: bool
    booking_id: str
    message: str
    payment_status: str
    payment_verified: bool
    total_amount: float