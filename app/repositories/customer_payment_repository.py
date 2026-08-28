from app.supabase.client import supabase


class CustomerPaymentRepository:

    # =========================================================
    # GET BOOKING FOR PAYMENT
    # =========================================================

    @staticmethod
    def get_booking_for_payment(
        booking_id: str,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select(
                """
                id,
                user_id,
                total_amount,
                payment_status,
                payment_verified,
                razorpay_order_id
                """
            )
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # SAVE RAZORPAY ORDER
    # =========================================================

    @staticmethod
    def save_razorpay_order(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "payment_status": "pending",
                    "payment_verified": False,
                }
            )
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data[0] if response.data else None

    # =========================================================
    # COMPLETE PAYMENT
    # =========================================================

    @staticmethod
    def complete_payment(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
        payment_method: str | None = None,
    ):

        data = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
            "payment_status": "paid",
            "payment_verified": True,
        }

        if payment_method:
            data["payment_method"] = payment_method

        response = (
            supabase
            .table("bookings")
            .update(data)
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data[0] if response.data else None