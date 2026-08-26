from app.supabase.client import supabase


class AuthRepository:

    @staticmethod
    def login(email: str, password: str):
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        return response

    @staticmethod
    def get_user(access_token: str):
        response = supabase.auth.get_user(access_token)

        return response.user

    @staticmethod
    def logout():
        return supabase.auth.sign_out()