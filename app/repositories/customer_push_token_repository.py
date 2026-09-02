from app.supabase.client import supabase


class CustomerPushTokenRepository:

    # =========================================================
    # REMOVE TOKEN FROM ANY USER
    # =========================================================

    @staticmethod
    def delete_by_token(token: str):

        response = (
            supabase
            .table("push_tokens")
            .delete()
            .eq("token", token)
            .execute()
        )

        return response.data

    # =========================================================
    # UPSERT CUSTOMER TOKEN
    # =========================================================

    @staticmethod
    def upsert_token(
        user_id: str,
        token: str,
        platform: str,
    ):

        response = (
            supabase
            .table("push_tokens")
            .upsert(
                {
                    "user_id": user_id,
                    "token": token,
                    "platform": platform,
                },
                on_conflict="user_id",
            )
            .execute()
        )

        return response.data

    # =========================================================
    # DELETE CUSTOMER TOKEN
    # =========================================================

    @staticmethod
    def delete_token(
        user_id: str,
        token: str,
    ):

        response = (
            supabase
            .table("push_tokens")
            .delete()
            .eq("user_id", user_id)
            .eq("token", token)
            .execute()
        )

        return response.data