# from fastapi import HTTPException

# from app.repositories.partner_zone_repository import (
#     PartnerZoneRepository,
# )


# class PartnerZoneService:

#     # =========================================================
#     # GET ZONE
#     # =========================================================

#     @staticmethod
#     def get_zone(email: str):

#         zone = PartnerZoneRepository.get_partner_zone(
#             email=email
#         )

#         if not zone:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Unable to find assigned zone.",
#             )

#         return zone

#     # =========================================================
#     # UPDATE LOCATION
#     # =========================================================

#     @staticmethod
#     def update_location(
#         email: str,
#         live_location: str | None = None,
#         is_out_of_zone: bool | None = None,
#     ):

#         PartnerZoneRepository.update_location(
#             email=email,
#             live_location=live_location,
#             is_out_of_zone=is_out_of_zone,
#         )

#         return {
#             "success": True,
#             "message": "Partner location updated successfully.",
#         }








from fastapi import HTTPException

from app.repositories.partner_zone_repository import (
    PartnerZoneRepository,
)


class PartnerZoneService:

    # =========================================================
    # GET PARTNER ZONE
    # =========================================================

    @staticmethod
    def get_zone(email: str):

        zone = (
            PartnerZoneRepository.get_partner_zone(
                email=email
            )
        )

        if not zone:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Unable to find assigned zone."
                ),
            )

        # IMPORTANT:
        # Do NOT wrap this in {"success": True, "data": ...}
        #
        # Your partner router already does that.
        #

        return zone

    # =========================================================
    # UPDATE LOCATION
    # =========================================================

    @staticmethod
    def update_location(
        email: str,
        live_location: str | None = None,
        is_out_of_zone: bool | None = None,
    ):

        PartnerZoneRepository.update_location(
            email=email,
            live_location=live_location,
            is_out_of_zone=is_out_of_zone,
        )

        return {
            "success": True,
            "message": (
                "Partner location updated successfully."
            ),
        }