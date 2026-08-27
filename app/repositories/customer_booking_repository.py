from app.supabase.client import supabase


class CustomerBookingRepository:

    @staticmethod
    def create_booking(payload: dict):
        response = (
            supabase
            .table("bookings")
            .insert(payload)
            .execute()
        )

        return response.data

    @staticmethod
    def get_customer_bookings(user_id: str):
        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    @staticmethod
    def get_booking(
        booking_id: str,
    ):
        response = (
            supabase
            .table("bookings")
            .select("*")
            .eq("id", booking_id)
            .maybe_single()
            .execute()
        )

        return response.data

    @staticmethod
    def cancel_booking(
        booking_id: str,
    ):
        response = (
            supabase
            .table("bookings")
            .update(
                {
                    "work_status": "cancelled",
                }
            )
            .eq("id", booking_id)
            .execute()
        )

        return response.data