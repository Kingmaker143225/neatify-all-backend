# from fastapi import APIRouter, Depends

# from app.dependencies.admin import (
#     get_current_admin,
# )

# from app.schemas.admin_auth import (
#     AdminLoginRequest,
#     AdminLoginResponse,
#     AdminMeResponse,
# )

# from app.services.admin_auth_service import (
#     AdminAuthService,
# )


# router = APIRouter()


# # =========================================================
# # ADMIN LOGIN
# # =========================================================

# @router.post(
#     "/auth/login",
#     response_model=AdminLoginResponse,
# )
# async def admin_login(
#     request: AdminLoginRequest,
# ):

#     return AdminAuthService.login(
#         email=request.email,
#         password=request.password,
#     )


# # =========================================================
# # ADMIN ME
# # =========================================================

# @router.get(
#     "/auth/me",
#     response_model=AdminMeResponse,
# )
# async def admin_me(
#     current_admin=Depends(
#         get_current_admin
#     ),
# ):

#     profile = current_admin["profile"]
#     user = current_admin["user"]

#     return {
#         "id": str(
#             user.id
#         ),
#         "email": (
#             user.email
#             or profile.get("email")
#             or ""
#         ),
#     }















# from fastapi import (
#     APIRouter,
#     Depends,
# )

# from app.dependencies.admin import (
#     get_current_admin,
# )

# from app.schemas.admin_auth import (
#     AdminLoginRequest,
#     AdminLoginResponse,
#     AdminMeResponse,
# )

# from app.services.admin_auth_service import (
#     AdminAuthService,
# )


# # =========================================================
# # ROUTER
# # =========================================================

# router = APIRouter()


# # =========================================================
# # ADMIN LOGIN
# # =========================================================

# @router.post(
#     "/auth/login",
#     response_model=AdminLoginResponse,
# )
# async def admin_login(
#     request: AdminLoginRequest,
# ):
#     return AdminAuthService.login(
#         email=request.email,
#         password=request.password,
#     )


# # =========================================================
# # ADMIN ME
# # =========================================================

# @router.get(
#     "/auth/me",
#     response_model=AdminMeResponse,
# )
# async def admin_me(
#     current_admin=Depends(
#         get_current_admin
#     ),
# ):
#     profile = current_admin["profile"]
#     user = current_admin["user"]

#     return {
#         "id": str(user.id),
#         "email": (
#             user.email
#             or profile.get("email")
#             or ""
#         ),
#     }


# # =========================================================
# # ADMIN LOGOUT
# # =========================================================

# @router.post(
#     "/auth/logout"
# )
# async def admin_logout(
#     current_admin=Depends(
#         get_current_admin
#     ),
# ):
#     return {
#         "success": True,
#         "message": "Admin logged out successfully.",
#     }














from app.schemas.admin_profile import (
    AdminProfileResponse,
    AdminProfileUpdateRequest,
)

from app.services.admin_profile_service import (
    AdminProfileService,
)
from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies.admin import (
    get_current_admin,
)

from app.schemas.admin_auth import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminMeResponse,
)

from app.services.admin_auth_service import (
    AdminAuthService,
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter()


# =========================================================
# ADMIN LOGIN
# =========================================================

@router.post(
    "/auth/login",
    response_model=AdminLoginResponse,
)
async def admin_login(
    request: AdminLoginRequest,
):
    return AdminAuthService.login(
        email=request.email,
        password=request.password,
    )


# =========================================================
# ADMIN ME
# =========================================================

@router.get(
    "/auth/me",
    response_model=AdminMeResponse,
)
async def admin_me(
    current_admin=Depends(
        get_current_admin
    ),
):
    profile = current_admin["profile"]
    user = current_admin["user"]

    return {
        "id": str(user.id),
        "email": (
            user.email
            or profile.get("email")
            or ""
        ),
    }


# =========================================================
# ADMIN LOGOUT
# =========================================================

@router.post(
    "/auth/logout"
)
async def admin_logout(
    current_admin=Depends(
        get_current_admin
    ),
):
    return {
        "success": True,
        "message": "Admin logged out successfully.",
    }

# =========================================================
# ADMIN PROFILE
# =========================================================

@router.get(
    "/profile",
    response_model=AdminProfileResponse,
)
async def get_admin_profile(
    current_admin=Depends(
        get_current_admin
    ),
):

    return (
        AdminProfileService
        .get_profile(
            admin=current_admin,
        )
    )


# =========================================================
# UPDATE ADMIN PROFILE
# =========================================================

@router.put(
    "/profile",
    response_model=AdminProfileResponse,
)
async def update_admin_profile(
    request: AdminProfileUpdateRequest,
    current_admin=Depends(
        get_current_admin
    ),
):

    return (
        AdminProfileService
        .update_profile(
            admin=current_admin,
            full_name=request.full_name,
            phone=request.phone,
            address=request.address,
            pincode=request.pincode,
        )
    )