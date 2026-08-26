from fastapi import HTTPException, status

from app.repositories.partner_booking_repository import (
    PartnerBookingRepository,
)


class PartnerBookingActionService:

    @staticmethod
    def _get_pending_booking(
        booking_id: str,
        email: str,
    ):
        booking = (
            PartnerBookingRepository
            .get_booking_for_partner(
                booking_id=booking_id,
                email=email,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found.",
            )

        staff_response = booking.get("staff_response")
        work_status = booking.get("work_status")

        # Booking must still be pending.
        if staff_response not in (None, "pending", "PENDING"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This booking has already been responded to.",
            )

        # Never allow actions on completed/cancelled bookings.
        if work_status in ("COMPLETED", "CANCELLED"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This booking is no longer active.",
            )

        return booking


    @staticmethod
    def approve(
        booking_id: str,
        email: str,
    ):
        PartnerBookingActionService._get_pending_booking(
            booking_id=booking_id,
            email=email,
        )

        result = (
            PartnerBookingRepository
            .approve_booking(
                booking_id=booking_id,
                email=email,
            )
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to approve booking.",
            )

        return {
            "success": True,
            "message": "Booking approved successfully.",
            "booking_id": booking_id,
        }


    @staticmethod
    def reject(
        booking_id: str,
        email: str,
        reason: str,
    ):
        PartnerBookingActionService._get_pending_booking(
            booking_id=booking_id,
            email=email,
        )

        result = (
            PartnerBookingRepository
            .reject_booking(
                booking_id=booking_id,
                email=email,
                reason=reason,
            )
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to reject booking.",
            )

        return {
            "success": True,
            "message": "Booking rejected successfully.",
            "booking_id": booking_id,
        }

    # =============================================================
    # CANCEL ASSIGNED BOOKING
    # =============================================================

    @staticmethod
    def cancel(
        booking_id: str,
        email: str,
        reason: str,
    ):
        # ---------------------------------------------------------
        # Get booking
        # ---------------------------------------------------------

        booking = (
            PartnerBookingRepository
            .get_booking_for_partner(
                booking_id=booking_id,
                email=email,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found.",
            )

        # ---------------------------------------------------------
        # Current booking state
        # ---------------------------------------------------------

        staff_response = booking.get("staff_response")
        work_status = booking.get("work_status")

        # ---------------------------------------------------------
        # Only APPROVED bookings can be cancelled
        # ---------------------------------------------------------

        if staff_response != "APPROVED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Only assigned/approved services "
                    "can be cancelled."
                ),
            )

        # ---------------------------------------------------------
        # Only ASSIGNED bookings can be cancelled
        # ---------------------------------------------------------

        if work_status != "ASSIGNED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Only assigned services "
                    "can be cancelled."
                ),
            )

        # ---------------------------------------------------------
        # Validate cancellation reason
        # ---------------------------------------------------------

        allowed_reasons = {
            "Medical Emergency",
            "Personal Emergency",
            "Vehicle Issue",
            "Traffic Delay",
            "Location Too Far",
            "Safety Concern",
            "Mobile Issue",
            "Other (specify)", 

        }

        if reason not in allowed_reasons:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid cancellation reason.",
            )

        # ---------------------------------------------------------
        # Cancel booking
        # ---------------------------------------------------------

        result = (
            PartnerBookingRepository
            .cancel_booking(
                booking_id=booking_id,
                email=email,
                reason=reason,
                cancellation_fee=99,
            )
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to cancel booking.",
            )

        # ---------------------------------------------------------
        # Success
        # ---------------------------------------------------------

        return {
            "success": True,
            "message": "Service cancelled successfully.",
            "booking_id": booking_id,
            "work_status": "CANCELLED",
            "cancel_reason": reason,
            "cancellation_fee": 99,
        }
        