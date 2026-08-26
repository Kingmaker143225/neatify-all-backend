# from fastapi import Depends

# from app.dependencies.auth import get_current_user
# from app.services.partner_service import PartnerService


# async def get_current_partner(
#     current_user=Depends(get_current_user),
# ):
#     return PartnerService.get_current_partner(
#         str(current_user.id)
#     )

from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.services.partner_service import PartnerService


async def get_current_partner(
    current_user=Depends(get_current_user),
):
    return PartnerService.get_current_partner(
        str(current_user.id)
    )