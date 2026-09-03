from fastapi import HTTPException, status

from app.supabase.client import supabase

from app.repositories.admin_repository import (
    AdminRepository,
)


class AdminAuthService:

    # =========================================================
    # ADMIN LOGIN
    # =========================================================

    @staticmethod
    def login(
        email: str,
        password: str,
    ):

        # -----------------------------------------------------
        # SUPABASE AUTHENTICATION
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # CHECK SESSION
        # -----------------------------------------------------

        if (
            not response.session
            or not response.user
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        user = response.user
        session = response.session

        # -----------------------------------------------------
        # ADMIN AUTHORIZATION
        #
        # User must exist in admin_profile.
        # -----------------------------------------------------

        admin = (
            AdminRepository
            .get_by_id(
                str(user.id)
            )
        )

        if not admin:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "This account is not authorized "
                    "to access the Admin Dashboard."
                ),
            )

        # -----------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
        }