# from fastapi import Depends, HTTPException, status
# from fastapi.security import (
#     HTTPAuthorizationCredentials,
#     HTTPBearer,
# )

# from app.services.customer_auth_service import (
#     CustomerAuthService,
# )


# customer_security = HTTPBearer()


# async def get_current_customer(
#     credentials: HTTPAuthorizationCredentials = Depends(
#         customer_security
#     ),
# ):
#     access_token = credentials.credentials

#     user = (
#         CustomerAuthService
#         .get_current_user(
#             access_token
#         )
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication token.",
#         )

#     return {
#         "id": str(user.id),
#         "email": user.email or "",
#         "user": user,
#         "access_token": access_token,
#     }




















from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.services.customer_auth_service import (
    CustomerAuthService,
)


customer_security = HTTPBearer()


async def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(
        customer_security
    ),
):
    access_token = credentials.credentials

    user = (
        CustomerAuthService
        .get_current_user(
            access_token
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )

    return {
        "id": str(user.id),
        "email": user.email or "",
        "user": user,
        "access_token": access_token,
    }