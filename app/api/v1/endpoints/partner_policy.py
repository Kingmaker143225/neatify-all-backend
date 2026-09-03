from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user

from app.schemas.partner_policy import (
    PolicyResponse,
    AcceptPolicyResponse,
    PolicyStatusResponse,
)

from app.services.partner_policy_service import (
    PartnerPolicyService,
)

router = APIRouter()


@router.get(
    "/policies",
    response_model=PolicyResponse,
)
async def get_policies():

    return (
        PartnerPolicyService
        .get_active_partner_policies()
    )


@router.patch(
    "/policies/accept",
    response_model=AcceptPolicyResponse,
)
async def accept_policies(
    current_user=Depends(
        get_current_user
    ),
):

    return (
        PartnerPolicyService
        .accept_policies(
            str(current_user.id)
        )
    )

@router.get(
    "/policies/status",
    response_model=PolicyStatusResponse,
)
async def get_policy_status(
    current_user=Depends(
        get_current_user
    ),
):

    return (
        PartnerPolicyService
        .get_policy_status(
            str(current_user.id)
        )
    )