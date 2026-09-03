from app.supabase.admin_client import supabase_admin


class BookingReminderRepository:

    @staticmethod
    def get_future_bookings(now_iso: str):
        response = (
            supabase_admin
            .table("bookings")
            .select("*")
            .gte("booking_schedule_at", now_iso)
            .order("booking_schedule_at", desc=False)
            .execute()
        )

        return response.data or []

    @staticmethod
    def get_staff_by_email(email: str):
        response = (
            supabase_admin
            .table("staff_profile")
            .select("push_token,name")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        return response.data

    @staticmethod
    def create_notification(data: dict):
        response = (
            supabase_admin
            .table("notifications")
            .insert(data)
            .execute()
        )

        return response.data

    @staticmethod
    def update_reminder_flags(
        booking_id: str,
        update_data: dict,
    ):
        response = (
            supabase_admin
            .table("bookings")
            .update(update_data)
            .eq("id", booking_id)
            .execute()
        )

        return response.data