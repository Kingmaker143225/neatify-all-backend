import razorpay

from fastapi import HTTPException, status

from app.config.settings import settings

from app.repositories.customer_payment_repository import (
    CustomerPaymentRepository,
)


class CustomerPaymentService:

    # =========================================================
    # RAZORPAY CLIENT
    # =========================================================

    @staticmethod
    def get_razorpay_client():

        if not settings.razorpay_key_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Razorpay key ID is not configured.",
            )

        if not settings.razorpay_key_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Razorpay secret key is not configured.",
            )

        return razorpay.Client(
            auth=(
                settings.razorpay_key_id,
                settings.razorpay_key_secret,
            )
        )

    # =========================================================
    # CREATE ORDER
    # =========================================================

    @staticmethod
    def create_order(
        booking_id: str,
        user_id: str,
    ):

        booking = (
            CustomerPaymentRepository
            .get_booking_for_payment(
                booking_id=booking_id,
                user_id=user_id,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found.",
            )

        if booking.get("payment_verified"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment is already completed.",
            )

        total_amount = booking.get(
            "total_amount"
        )

        if total_amount is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking amount is missing.",
            )

        if float(total_amount) <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid booking amount.",
            )

        # Razorpay accepts amount in paise.
        amount_paise = int(
            round(float(total_amount) * 100)
        )

        client = (
            CustomerPaymentService
            .get_razorpay_client()
        )

        try:

            razorpay_order = client.order.create(
                {
                    "amount": amount_paise,
                    "currency": "INR",
                    "receipt": str(booking_id),
                    "notes": {
                        "booking_id": str(
                            booking_id
                        ),
                        "user_id": str(
                            user_id
                        ),
                    },
                }
            )

        # except Exception as exc:

        #     print(
        #         "❌ Razorpay order creation failed:",
        #         str(exc),
        #     )

        #     raise HTTPException(
        #         status_code=status.HTTP_502_BAD_GATEWAY,
        #         detail="Unable to create Razorpay order.",
        #     ) from exc
        
        # except Exception as exc:
        #     print(
        #         "RAZORPAY ORDER ERROR:",
        #         repr(exc),
        #     )

        #     raise HTTPException(
        #         status_code=status.HTTP_502_BAD_GATEWAY,
        #         detail="Unable to create Razorpay order.",
        #     ) from 
        except Exception as exc:
            print("========================================")
            print("RAZORPAY ERROR:", repr(exc))
            print("RAZORPAY ERROR TYPE:", type(exc).__name__)
            print("========================================")

            raise HTTPException(
                status_code=502,
                detail=f"Unable to create Razorpay order: {exc}",
            ) from exc

        razorpay_order_id = razorpay_order.get(
            "id"
        )

        if not razorpay_order_id:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Razorpay did not return an order ID.",
            )

        saved_booking = (
            CustomerPaymentRepository
            .save_razorpay_order(
                booking_id=booking_id,
                user_id=user_id,
                razorpay_order_id=razorpay_order_id,
            )
        )

        if not saved_booking:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Razorpay order created but booking could not be updated.",
            )

        return {
            "success": True,
            "booking_id": str(booking_id),
            "razorpay_order_id": razorpay_order_id,
            "amount": amount_paise,
            "currency": "INR",
            "razorpay_key_id": settings.razorpay_key_id,
        }

    # =========================================================
    # VERIFY PAYMENT
    # =========================================================

    @staticmethod
    def verify_payment(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ):

        booking = (
            CustomerPaymentRepository
            .get_booking_for_payment(
                booking_id=booking_id,
                user_id=user_id,
            )
        )

        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found.",
            )

        stored_order_id = booking.get(
            "razorpay_order_id"
        )

        if not stored_order_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Razorpay order exists for this booking.",
            )

        if stored_order_id != razorpay_order_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Razorpay order does not match booking.",
            )

        if not razorpay_payment_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Razorpay payment ID is required.",
            )

        if not razorpay_signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Razorpay signature is required.",
            )

        client = (
            CustomerPaymentService
            .get_razorpay_client()
        )

        try:

            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": (
                        razorpay_order_id
                    ),
                    "razorpay_payment_id": (
                        razorpay_payment_id
                    ),
                    "razorpay_signature": (
                        razorpay_signature
                    ),
                }
            )

        except Exception as exc:

            print(
                "❌ Razorpay signature verification failed:",
                str(exc),
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed.",
            ) from exc

        updated_booking = (
            CustomerPaymentRepository
            .complete_payment(
                booking_id=booking_id,
                user_id=user_id,
                razorpay_order_id=(
                    razorpay_order_id
                ),
                razorpay_payment_id=(
                    razorpay_payment_id
                ),
                razorpay_signature=(
                    razorpay_signature
                ),
            )
        )

        if not updated_booking:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment verified but booking could not be updated.",
            )

        return {
            "success": True,
            "booking_id": str(booking_id),
            "payment_status": "paid",
            "payment_verified": True,
            "message": "Payment verified successfully.",
        }