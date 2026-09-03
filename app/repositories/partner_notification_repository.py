from app.supabase.client import supabase


class PartnerNotificationRepository:

    @staticmethod
    def get_notifications(staff_email: str):
        response = (
            supabase
            .table("notifications")
            .select("*")
            .eq("staff_email", staff_email)
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    @staticmethod
    def mark_as_read(
        notification_id: str,
        staff_email: str,
    ):
        response = (
            supabase
            .table("notifications")
            .update({
                "is_read": True,
            })
            .eq("id", notification_id)
            .eq("staff_email", staff_email)
            .select()
            .execute()
        )

        return response.data or []

    @staticmethod
    def delete_notification(
        notification_id: str,
        staff_email: str,
    ):
        response = (
            supabase
            .table("notifications")
            .delete()
            .eq("id", notification_id)
            .eq("staff_email", staff_email)
            .execute()
        )

        return response.data or []

    @staticmethod
    def delete_all_notifications(
        staff_email: str,
    ):
        response = (
            supabase
            .table("notifications")
            .delete()
            .eq("staff_email", staff_email)
            .execute()
        )

        return response.data or []

    @staticmethod
    def create_notification(data: dict):
        response = (
            supabase
            .table("notifications")
            .insert(data)
            .execute()
        )

        return response.data or []