from fastapi import APIRouter, Query

from app.schemas.customer_service import (
    CustomerMainCategoryResponse,
    CustomerServiceResponse,
    CustomerAddOnResponse,
)

from app.services.customer_service_service import (
    CustomerServiceService,
)


router = APIRouter()


# =========================================================
# MAIN CATEGORIES
# =========================================================

@router.get(
    "/categories",
    response_model=list[
        CustomerMainCategoryResponse
    ],
)
async def get_customer_categories():

    return (
        CustomerServiceService
        .get_main_categories()
    )


# =========================================================
# SERVICES
# =========================================================

@router.get(
    "/services",
    response_model=list[
        CustomerServiceResponse
    ],
)
async def get_customer_services(
    main_category_id: str | None = Query(
        default=None,
    ),
    service_type: str | None = Query(
        default=None,
    ),
):

    return (
        CustomerServiceService
        .get_services(
            main_category_id=main_category_id,
            service_type=service_type,
        )
    )


# =========================================================
# SERVICE BY SLUG
#
# IMPORTANT:
# This route must appear before /{service_id}
# =========================================================

@router.get(
    "/services/slug/{slug}",
    response_model=CustomerServiceResponse,
)
async def get_customer_service_by_slug(
    slug: str,
):

    return (
        CustomerServiceService
        .get_service_by_slug(
            slug=slug,
        )
    )


# =========================================================
# SERVICE BY ID
# =========================================================

@router.get(
    "/services/{service_id}",
    response_model=CustomerServiceResponse,
)
async def get_customer_service_by_id(
    service_id: str,
):

    return (
        CustomerServiceService
        .get_service_by_id(
            service_id=service_id,
        )
    )


# =========================================================
# ACTIVE ADD-ONS
# =========================================================

@router.get(
    "/add-ons",
    response_model=list[
        CustomerAddOnResponse
    ],
)
async def get_customer_addons(
    service_type: str | None = Query(
        default=None,
    ),
):

    return (
        CustomerServiceService
        .get_active_addons(
            service_type=service_type,
        )
    )