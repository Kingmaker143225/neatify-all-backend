from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_profile import (
    CustomerProfileResponse,
    CustomerProfileUpdateRequest,
)

from app.services.customer_profile_service import (
    CustomerProfileService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER PROFILE
# =========================================================

@router.get(
    "",
    response_model=CustomerProfileResponse,
)
async def get_customer_profile(
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerProfileService
        .get_profile(
            customer=current_customer,
        )
    )


# =========================================================
# UPDATE CUSTOMER PROFILE
# =========================================================

@router.put(
    "",
    response_model=CustomerProfileResponse,
)
async def update_customer_profile(
    request: CustomerProfileUpdateRequest,
    current_customer=Depends(
        get_current_customer
    ),
):
    return (
        CustomerProfileService
        .update_profile(
            customer=current_customer,
            full_name=request.full_name,
            phone=request.phone,
            address=request.address,
            pincode=request.pincode,
        )
    )