from app.supabase.client import supabase


class CustomerRepository:

    # =========================================================
    # GET CUSTOMER PROFILE
    # =========================================================

    @staticmethod
    def get_profile(user_id: str):
        response = (
            supabase
            .table("profile")
            .select(
                """
                id,
                full_name,
                email,
                phone
                """
            )
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # CHECK CUSTOMER PROFILE EXISTS
    # =========================================================

    @staticmethod
    def profile_exists(user_id: str) -> bool:
        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        return profile is not None
    