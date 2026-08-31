from app.supabase.client import supabase


class CustomerPolicyRepository:

    @staticmethod
    def get_active_policy():
        response = (
            supabase
            .table("app_policies")
            .select(
                """
                id,
                user_policies,
                terms_and_conditions,
                is_active,
                created_at,
                updated_at
                """
            )
            .eq("is_active", True)
            .order(
                "updated_at",
                desc=True,
            )
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]