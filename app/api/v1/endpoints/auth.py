# from fastapi import APIRouter, HTTPException

# from app.schemas.auth import LoginRequest, LoginResponse
# from app.services.auth_service import AuthService

# router = APIRouter()


# @router.post("/login", response_model=LoginResponse)
# async def login(request: LoginRequest):

#     try:
#         return AuthService.login(
#             email=request.email,
#             password=request.password,
#         )

#     except Exception:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid email or password",
#         )








# from fastapi import APIRouter, Depends, HTTPException

# from app.dependencies.auth import get_current_user
# from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
# from app.services.auth_service import AuthService


# router = APIRouter()


# @router.post("/login", response_model=LoginResponse)
# async def login(request: LoginRequest):

#     try:
#         return AuthService.login(
#             email=request.email,
#             password=request.password,
#         )

#     except Exception:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid email or password",
#         )


# @router.get("/me", response_model=UserResponse)
# async def get_me(current_user=Depends(get_current_user)):

#     return UserResponse(
#         id=str(current_user.id),
#         email=current_user.email,
#     )





from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.dependencies.auth import get_current_user

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    CurrentUserResponse,
    LogoutResponse,
)

from app.services.auth_service import AuthService


router = APIRouter()

security = HTTPBearer()


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
):
    return AuthService.login(
        email=request.email,
        password=request.password,
    )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
async def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }


@router.post(
    "/logout",
    response_model=LogoutResponse,
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    current_user=Depends(get_current_user),
):
    return AuthService.logout(
        credentials.credentials
    )