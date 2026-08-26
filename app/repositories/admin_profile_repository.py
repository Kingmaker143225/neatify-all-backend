from app.supabase.client import supabase


class AdminProfileRepository:

    # =========================================================
    # GET ADMIN PROFILE
    # =========================================================

    @staticmethod
    def get_profile(
        user_id: str,
    ):

        # -----------------------------------------------------
        # ADMIN SIGNUP
        # -----------------------------------------------------

        signup_response = (
            supabase
            .table("admin_signup")
            .select(
                "full_name, email, phone"
            )
            .eq(
                "id",
                user_id,
            )
            .maybe_single()
            .execute()
        )

        signup_data = (
            signup_response.data
            or {}
        )

        # -----------------------------------------------------
        # ADMIN PROFILE
        # -----------------------------------------------------

        profile_response = (
            supabase
            .table("admin_profile")
            .select("*")
            .eq(
                "id",
                user_id,
            )
            .maybe_single()
            .execute()
        )

        profile_data = (
            profile_response.data
            or {}
        )

        return {
            "signup": signup_data,
            "profile": profile_data,
        }

    # =========================================================
    # UPDATE ADMIN PROFILE
    # =========================================================

    @staticmethod
    def update_profile(
        user_id: str,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
    ):

        # -----------------------------------------------------
        # UPDATE ADMIN PROFILE
        # -----------------------------------------------------

        profile_response = (
            supabase
            .table("admin_profile")
            .upsert(
                {
                    "id": user_id,
                    "full_name": (
                        full_name
                        or None
                    ),
                    "phone": (
                        phone
                        or None
                    ),
                    "address": (
                        address
                        or None
                    ),
                    "pincode": (
                        pincode
                        or None
                    ),
                }
            )
            .execute()
        )

        # -----------------------------------------------------
        # UPDATE ADMIN SIGNUP
        # -----------------------------------------------------

        signup_response = (
            supabase
            .table("admin_signup")
            .update(
                {
                    "full_name": full_name,
                    "phone": phone,
                }
            )
            .eq(
                "id",
                user_id,
            )
            .execute()
        )

        return {
            "profile": (
                profile_response.data
                or []
            ),
            "signup": (
                signup_response.data
                or []
            ),
        }