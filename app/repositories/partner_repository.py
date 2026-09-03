from app.supabase.client import supabase


class PartnerRepository:

    @staticmethod
    def get_by_id(user_id: str):
        response = (
            supabase
            .table("staff_profile")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data