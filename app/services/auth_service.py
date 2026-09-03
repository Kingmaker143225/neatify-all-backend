from fastapi import HTTPException, status

from app.supabase.client import supabase


class AuthService:

    # =========================================================
    # LOGIN
    # =========================================================

    @staticmethod
    def login(
        email: str,
        password: str,
    ):
        try:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
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

        # =====================================================
        # PARTNER AUTHORIZATION
        # =====================================================

        staff_response = (
            supabase
            .table("staff_profile")
            .select("id, is_blocked")
            .eq("id", str(user.id))
            .maybe_single()
            .execute()
        )

        staff = staff_response.data

        # User exists in Auth but not in staff_profile
        if not staff:

            try:
                supabase.auth.sign_out()
            except Exception:
                pass

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "This account is not authorized "
                    "to access the Partner App."
                ),
            )

        # Partner is blocked
        if staff.get("is_blocked") is True:

            try:
                supabase.auth.sign_out()
            except Exception:
                pass

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your partner account is blocked.",
            )

        # =====================================================
        # SUCCESS
        # =====================================================

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
        }

    # =========================================================
    # GET CURRENT USER
    # =========================================================

    @staticmethod
    def get_current_user(
        access_token: str,
    ):

        try:
            response = supabase.auth.get_user(
                access_token
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
    # LOGOUT
    # =========================================================

    @staticmethod
    def logout(
        access_token: str,
    ):

        try:
            # Validate the access token first.
            user_response = supabase.auth.get_user(
                access_token
            )

            if not user_response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired access token.",
                )

            # -------------------------------------------------
            # Logout is handled by the Partner App by clearing
            # its locally stored access/refresh tokens after
            # receiving this successful response.
            #
            # Supabase access tokens are JWTs and may remain
            # valid until their expiry.
            # -------------------------------------------------

            return {
                "success": True,
                "message": "Logged out successfully.",
            }

        except HTTPException:
            raise

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Logout failed.",
            ) from exc