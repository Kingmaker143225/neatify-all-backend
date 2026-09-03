from app.supabase.client import supabase


class AdminRepository:

    @staticmethod
    def get_by_id(user_id: str):

        response = (
            supabase
            .table("admin_profile")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data