# from fastapi import APIRouter, Depends

# from app.dependencies.auth import get_current_user
# from app.services.customer_promotional_banner_service import (
#     CustomerPromotionalBannerService,
# )

# router = APIRouter(
#     prefix="/customer",
#     tags=["Customer Promotional Banners"],
# )


# @router.get("/promotional-banners")
# async def get_customer_promotional_banners(
#     current_user=Depends(get_current_user),
# ):
#     return CustomerPromotionalBannerService.get_active_banners()












from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.services.customer_promotional_banner_service import (
    CustomerPromotionalBannerService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER PROMOTIONAL BANNERS
# =========================================================

@router.get(
    "/promotional-banners",
)
async def get_customer_promotional_banners(
    pincode: str | None = Query(
        default=None,
        description=(
            "Customer pincode used for promotional "
            "banner location eligibility."
        ),
    ),
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = str(
        current_customer["user"].id
    )

    return (
        CustomerPromotionalBannerService
        .get_active_banners(
            user_id=user_id,
            pincode=pincode,
        )
    )