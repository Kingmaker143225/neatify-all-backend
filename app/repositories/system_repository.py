from app.supabase.client import supabase


class SystemRepository:

    @staticmethod
    def test_connection():
        response = (
            supabase
            .table("admin_settings")
            .select("*")
            .limit(1)
            .execute()
        )

        return response.data