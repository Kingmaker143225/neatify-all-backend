from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.services.customer_home_service import (
    CustomerHomeService,
)


router = APIRouter()


# =========================================================
# CUSTOMER HERO BANNERS
# =========================================================

@router.get("/hero-banners")
async def get_customer_hero_banners(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerHomeService.get_hero_banners()


# =========================================================
# CUSTOMER POPUPS
# =========================================================

@router.get("/popups")
async def get_customer_popups(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerHomeService.get_popups()


# =========================================================
# CUSTOMER OFFERS
# =========================================================

@router.get("/offers")
async def get_customer_offers(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerHomeService.get_offers()

# =========================================================
# CUSTOMER WHY CHOOSE US
# =========================================================

@router.get("/why-choose-us")
async def get_customer_why_choose_us(
    current_customer=Depends(
        get_current_customer
    ),
):
    return CustomerHomeService.get_why_choose_us()