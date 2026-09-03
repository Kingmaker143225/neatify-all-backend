from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.services.auth_service import AuthService
from app.repositories.admin_repository import (
    AdminRepository,
)


security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):
    token = credentials.credentials

    # =========================================================
    # VALIDATE SUPABASE ACCESS TOKEN
    # =========================================================

    current_user = AuthService.get_current_user(
        token
    )

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )

    # =========================================================
    # CHECK ADMIN PROFILE
    # =========================================================

    admin = AdminRepository.get_by_id(
        str(current_user.id)
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    # Return both:
    # - admin profile
    # - authenticated Supabase user
    return {
        "profile": admin,
        "user": current_user,
    }


    # =========================================================
    # ADMIN LOGOUT
    # =========================================================

    @router.post("/auth/logout")
    async def admin_logout(
        current_admin=Depends(get_current_admin),
    ):
        return {
            "success": True,
            "message": "Admin logged out successfully.",
        }