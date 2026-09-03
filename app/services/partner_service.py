from fastapi import HTTPException, status

from app.repositories.partner_repository import PartnerRepository


class PartnerService:

    @staticmethod
    def get_current_partner(user_id: str):

        partner = PartnerRepository.get_by_id(user_id)

        if not partner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is not authorized to access the Partner App.",
            )

        if partner.get("is_blocked"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your partner account is blocked.",
            )

        return partner