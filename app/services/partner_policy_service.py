from app.supabase.client import supabase


class PartnerPolicyService:

    @staticmethod
    def get_active_partner_policies():

        response = (
            supabase
            .table("app_policies")
            .select(
                """
                user_policies,
                terms_and_conditions
                """
            )
            .eq("app_type", "partner")
            .eq("is_active", True)
            .order(
                "created_at",
                desc=True,
            )
            .limit(1)
            .single()
            .execute()
        )

        return response.data

    @staticmethod
    def accept_policies(
        user_id: str,
    ):

        (
            supabase
            .table("staff_profile")
            .update(
                {
                    "terms_accepted": True,
                    "privacy_policy_accepted": True,
                }
            )
            .eq("id", user_id)
            .execute()
        )

        return {
            "success": True,
        }

    @staticmethod
    def get_policy_status(
        user_id: str,
    ):

        response = (
            supabase
            .table("staff_profile")
            .select(
                """
                terms_accepted,
                privacy_policy_accepted
                """
            )
            .eq("id", user_id)
            .single()
            .execute()
        )

        return response.data

