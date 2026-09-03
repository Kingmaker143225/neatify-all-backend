from fastapi import HTTPException, status

from app.repositories.customer_repository import (
    CustomerRepository,
)
from app.supabase.client import supabase


class CustomerAuthService:

    # =========================================================
    # LOGIN
    # =========================================================

    @staticmethod
    def login(
        email: str,
        password: str,
    ):
        try:
            response = (
                supabase
                .auth
                .sign_in_with_password(
                    {
                        "email": email,
                        "password": password,
                    }
                )
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            ) from exc

        if not response.session or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        user = response.user
        session = response.session

        user_id = str(user.id)
        user_email = user.email or email

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user_id": user_id,
            "email": user_email,
            "profile_exists": profile is not None,
        }

    # =========================================================
    # GET CURRENT USER
    # =========================================================

    @staticmethod
    def get_current_user(
        access_token: str,
    ):
        try:
            response = (
                supabase
                .auth
                .get_user(access_token)
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token.",
            ) from exc

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token.",
            )

        return response.user

    # =========================================================
    # ME
    # =========================================================

    @staticmethod
    def get_me(
        access_token: str,
    ):
        user = (
            CustomerAuthService
            .get_current_user(
                access_token
            )
        )

        user_id = str(user.id)

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        return {
            "id": user_id,
            "email": user.email or "",
            "profile_exists": profile is not None,
            "profile": profile,
        }

    # =========================================================
    # LOGOUT
    # =========================================================

    @staticmethod
    def logout(
        access_token: str,
    ):
        # Validate the token before accepting logout.
        CustomerAuthService.get_current_user(
            access_token
        )

        # The mobile client will ultimately remove its
        # local Supabase session. We intentionally do not
        # call global supabase.auth.sign_out() here because
        # the backend Supabase client is shared by requests.

        return {
            "success": True,
            "message": "Customer logged out successfully.",
        }