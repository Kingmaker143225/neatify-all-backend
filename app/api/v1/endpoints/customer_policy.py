# from fastapi import APIRouter, Depends

# from app.dependencies.customer_auth import (
#     get_current_customer,
# )

# from app.services.customer_policy_service import (
#     CustomerPolicyService,
# )


# router = APIRouter()


# # =========================================================
# # GET CUSTOMER POLICIES
# # =========================================================

# @router.get(
#     "/policies",
# )
# async def get_customer_policies(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):

#     return (
#         CustomerPolicyService
#         .get_policy()
#     )



















from fastapi import APIRouter

from app.services.customer_policy_service import (
    CustomerPolicyService,
)


router = APIRouter()


# =========================================================
# GET CUSTOMER POLICIES
# =========================================================

@router.get(
    "/policies",
)
async def get_customer_policies():

    return (
        CustomerPolicyService
        .get_policy()
    )