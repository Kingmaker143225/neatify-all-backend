from fastapi import HTTPException

from app.repositories.customer_booking_repository import (
    CustomerBookingRepository,
)


class CustomerBookingService:

    @staticmethod
    def create_booking(
        customer,
        request,
    ):
        user = customer["user"]

        payload = {
            "user_id": str(user.id),

            "customer_name": request.customer_name,
            "email": user.email,

            "phone_number": request.phone_number,

            "full_address": request.full_address,

            "latitude": request.latitude,
            "longitude": request.longitude,

            "services": request.services,

            "booking_date": request.booking_date,
            "booking_time": request.booking_time,

            "booking_schedule_at":
                f"{request.booking_date} "
                f"{request.booking_time} +05:30",

            "total_amount": request.total_amount,

            "payment_status": "pending",
            "payment_method": "razorpay",

            "coupon_code":
                request.coupon_code,

            "coupon_discount_percentage":
                request.coupon_discount_percentage,

            "coupon_discount_amount":
                request.coupon_discount_amount,
        }

        result = (
            CustomerBookingRepository
            .create_booking(payload)
        )

        booking = result[0]

        return {
            "id": booking["id"],
            "payment_status": "pending",
            "message":
                "Booking created successfully.",
        }

    @staticmethod
    def list_bookings(customer):
        return (
            CustomerBookingRepository
            .get_customer_bookings(
                str(customer["user"].id)
            )
        )

    @staticmethod
    def get_booking(
        customer,
        booking_id: str,
    ):
        booking = (
            CustomerBookingRepository
            .get_booking(
                booking_id
            )
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found.",
            )

        if booking["user_id"] != str(customer["user"].id):
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        return booking

    @staticmethod
    def cancel_booking(
        customer,
        booking_id: str,
    ):
        booking = (
            CustomerBookingRepository
            .get_booking(
                booking_id
            )
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found.",
            )

        if booking["user_id"] != str(customer["user"].id):
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        CustomerBookingRepository.cancel_booking(
            booking_id
        )

        return {
            "success": True,
            "message":
                "Booking cancelled successfully.",
        }