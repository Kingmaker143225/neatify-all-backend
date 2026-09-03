# from fastapi import HTTPException, status

# from app.repositories.partner_dashboard_repository import (
#     PartnerDashboardRepository,
# )


# class PartnerDashboardService:

#     @staticmethod
#     def get_dashboard(user_id: str):

#         profile = PartnerDashboardRepository.get_profile(user_id)

#         if not profile:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Partner profile not found.",
#             )

#         if profile.get("is_blocked"):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Your partner account is blocked.",
#             )

#         email = profile.get("email")

#         if not email:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Partner email not found.",
#             )

#         booking_stats = (
#             PartnerDashboardRepository
#             .get_booking_stats(email)
#         )

#         earnings = (
#             PartnerDashboardRepository
#             .get_earnings(email)
#         )

#         return {
#             "success": True,

#             "bookings": booking_stats,

#             "duty": {
#                 "is_available": bool(
#                     profile.get("is_available") or False
#                 ),
#                 "today_minutes": int(
#                     profile.get("today_duty_minutes") or 0
#                 ),
#                 "weekly_minutes": int(
#                     profile.get("weekly_duty_minutes") or 0
#                 ),
#                 "monthly_minutes": int(
#                     profile.get("monthly_duty_minutes") or 0
#                 ),
#             },

#             "earnings": earnings,
#         }














from fastapi import HTTPException, status

from app.repositories.partner_dashboard_repository import (
    PartnerDashboardRepository,
)


class PartnerDashboardService:

    @staticmethod
    def get_dashboard(user_id: str):

        # =====================================================
        # 1. GET PARTNER PROFILE
        # =====================================================

        profile = (
            PartnerDashboardRepository
            .get_profile(user_id)
        )

        if not profile:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Partner profile not found.",
            )

        # =====================================================
        # 2. BLOCKED CHECK
        # =====================================================

        if profile.get("is_blocked"):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your partner account is blocked.",
            )

        # =====================================================
        # 3. GET EMAIL
        # =====================================================

        email = profile.get("email")

        if not email:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Partner email not found.",
            )

        # =====================================================
        # 4. GET BOOKING COUNTS
        # =====================================================

        booking_stats = (
            PartnerDashboardRepository
            .get_booking_stats(email)
        )

        # =====================================================
        # 5. GET EARNINGS
        # =====================================================

        earnings = (
            PartnerDashboardRepository
            .get_earnings(email)
        )

        # =====================================================
        # 6. BUILD DASHBOARD RESPONSE
        # =====================================================

        return {

            "success": True,

            "bookings": {

                "new": int(
                    booking_stats.get("new", 0)
                ),

                "assigned": int(
                    booking_stats.get("assigned", 0)
                ),

                "completed": int(
                    booking_stats.get("completed", 0)
                ),

                "cancelled": int(
                    booking_stats.get("cancelled", 0)
                ),
            },

            "duty": {

                "is_available": bool(
                    profile.get("is_available", False)
                ),

                "today_minutes": int(
                    profile.get(
                        "today_duty_minutes"
                    ) or 0
                ),

                "weekly_minutes": int(
                    profile.get(
                        "weekly_duty_minutes"
                    ) or 0
                ),

                "monthly_minutes": int(
                    profile.get(
                        "monthly_duty_minutes"
                    ) or 0
                ),
            },

            "earnings": {

                "total": float(
                    earnings.get("total", 0)
                ),

                "weekly": float(
                    earnings.get("weekly", 0)
                ),

                "monthly": float(
                    earnings.get("monthly", 0)
                ),
            },
        }