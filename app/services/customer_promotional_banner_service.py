# from app.repositories.customer_promotional_banner_repository import (
#     CustomerPromotionalBannerRepository,
# )


# class CustomerPromotionalBannerService:

#     @staticmethod
#     def get_active_banners():

#         banners = (
#             CustomerPromotionalBannerRepository
#             .get_active_banners()
#         )

#         return {
#             "success": True,
#             "items": banners,
#             "message": (
#                 "Promotional banners fetched successfully."
#             ),
#         }


















from app.repositories.customer_promotional_banner_repository import (
    CustomerPromotionalBannerRepository,
)


class CustomerPromotionalBannerService:

    # =========================================================
    # GET CUSTOMER PROMOTIONAL BANNERS
    # =========================================================

    @staticmethod
    def get_active_banners(
        user_id: str,
        pincode: str | None = None,
    ):

        banners = (
            CustomerPromotionalBannerRepository
            .get_active_banners(
                user_id=user_id,
                pincode=pincode,
            )
        )

        return {
            "success": True,
            "items": banners,
            "message": (
                "Promotional banners fetched successfully."
            ),
        }