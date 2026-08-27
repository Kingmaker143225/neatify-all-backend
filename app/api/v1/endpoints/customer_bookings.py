from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_booking import (
    CustomerCreateBookingRequest,
    CustomerBookingResponse,
    CustomerCancelBookingResponse,
)

from app.services.customer_booking_service import (
    CustomerBookingService,
)


router = APIRouter()


@router.post(
    "",
    response_model=CustomerBookingResponse,
)
async def create_booking(
    request: CustomerCreateBookingRequest,
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerBookingService
        .create_booking(
            current_customer,
            request,
        )
    )


@router.get("")
async def list_bookings(
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerBookingService
        .list_bookings(
            current_customer
        )
    )


@router.get("/{booking_id}")
async def booking_details(
    booking_id: str,
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerBookingService
        .get_booking(
            current_customer,
            booking_id,
        )
    )


@router.post(
    "/{booking_id}/cancel",
    response_model=
    CustomerCancelBookingResponse,
)
async def cancel_booking(
    booking_id: str,
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerBookingService
        .cancel_booking(
            current_customer,
            booking_id,
        )
    )