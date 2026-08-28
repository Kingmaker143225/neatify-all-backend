from fastapi import HTTPException, status

from app.repositories.customer_booking_repository import (
    CustomerBookingRepository,
)


class CustomerBookingService:

    @staticmethod
    def create_booking(
        user_id: str,
        customer_name: str,
        email: str,
        phone_number: str,
        full_address: str,
        services,
        booking_date: str,
        booking_time: str,
        total_amount: float,
    ):

        customer_name = customer_name.strip()
        email = email.strip()
        phone_number = phone_number.strip()
        full_address = full_address.strip()

        if not customer_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer name is required.",
            )

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required.",
            )

        if not phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is required.",
            )

        if not full_address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address is required.",
            )

        if total_amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking amount must be greater than zero.",
            )

        booking = (
            CustomerBookingRepository
            .create_booking(
                customer_name=customer_name,
                email=email,
                phone_number=phone_number,
                full_address=full_address,
                services=services,
                booking_date=booking_date,
                booking_time=booking_time,
                total_amount=total_amount,
                user_id=user_id,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create booking.",
            )

        return {
            "success": True,
            "booking_id": str(booking["id"]),
            "message": "Booking created successfully.",
            "payment_status": booking.get(
                "payment_status",
                "pending",
            ),
            "payment_verified": bool(
                booking.get(
                    "payment_verified",
                    False,
                )
            ),
        }