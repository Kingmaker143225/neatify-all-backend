from app.supabase.client import supabase


class CustomerBookingRepository:

    # =========================================================
    # CREATE BOOKING
    # =========================================================

    @staticmethod
    def create_booking(
        customer_name: str,
        email: str,
        phone_number: str,
        full_address: str,
        services,
        booking_date: str,
        booking_time: str,
        total_amount: float,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .insert(
                {
                    "customer_name": customer_name,
                    "email": email,
                    "phone_number": phone_number,
                    "full_address": full_address,
                    "services": services,
                    "booking_date": booking_date,
                    "booking_time": booking_time,
                    "total_amount": total_amount,
                    "user_id": user_id,

                    # Payment starts as unpaid.
                    "payment_status": "pending",
                    "payment_verified": False,
                }
            )
            .execute()
        )

        return response.data[0] if response.data else None

    # =========================================================
    # GET BOOKING
    # =========================================================

    @staticmethod
    def get_booking(
        booking_id: str,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # UPDATE RAZORPAY ORDER
    # =========================================================

    @staticmethod
    def set_razorpay_order(
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
    # MARK PAYMENT SUCCESS
    # =========================================================

    @staticmethod
    def mark_payment_success(
        booking_id: str,
        user_id: str,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
        payment_method: str | None = None,
    ):

        update_data = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
            "payment_status": "paid",
            "payment_verified": True,
        }

        if payment_method:
            update_data["payment_method"] = payment_method

        response = (
            supabase
            .table("bookings")
            .update(update_data)
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data[0] if response.data else None

    # =========================================================
    # MARK PAYMENT FAILED
    # =========================================================

    @staticmethod
    def mark_payment_failed(
        booking_id: str,
        user_id: str,
    ):

        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "payment_status": "failed",
                    "payment_verified": False,
                }
            )
            .eq("id", booking_id)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data[0] if response.data else None