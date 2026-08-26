# from app.supabase.client import supabase


# class PartnerDashboardRepository:

#     @staticmethod
#     def get_booking_stats(email: str):

#         # NEW / UNVIEWED
#         new_response = (
#             supabase
#             .table("bookings")
#             .select("id", count="exact")
#             .eq("assigned_staff_email", email)
#             .eq("is_viewed", False)
#             .execute()
#         )

#         new_count = new_response.count or 0

#         # ASSIGNED
#         assigned_response = (
#             supabase
#             .table("bookings")
#             .select("id", count="exact")
#             .eq("assigned_staff_email", email)
#             .neq("work_status", "COMPLETED")
#             .neq("work_status", "CANCELLED")
#             .execute()
#         )

#         assigned_count = assigned_response.count or 0

#         # COMPLETED
#         completed_response = (
#             supabase
#             .table("bookings")
#             .select("id", count="exact")
#             .eq("assigned_staff_email", email)
#             .eq("work_status", "COMPLETED")
#             .execute()
#         )

#         completed_count = completed_response.count or 0

#         # CANCELLED
#         cancellation_response = (
#             supabase
#             .table("staff_cancellations")
#             .select("id", count="exact")
#             .eq("staff_email", email)
#             .execute()
#         )

#         cancelled_count = cancellation_response.count or 0

#         # Same fallback logic as Partner App
#         if cancelled_count == 0:

#             cancelled_bookings = (
#                 supabase
#                 .table("bookings")
#                 .select("id", count="exact")
#                 .eq("assigned_staff_email", email)
#                 .eq("work_status", "CANCELLED")
#                 .execute()
#             )

#             cancelled_count = cancelled_bookings.count or 0

#         return {
#             "new": new_count,
#             "assigned": assigned_count,
#             "completed": completed_count,
#             "cancelled": cancelled_count,
#         }

#     @staticmethod
#     def get_profile(user_id: str):

#         response = (
#             supabase
#             .table("staff_profile")
#             .select(
#                 """
#                 id,
#                 email,
#                 is_available,
#                 is_blocked,
#                 today_duty_minutes,
#                 weekly_duty_minutes,
#                 monthly_duty_minutes,
#                 total_earnings,
#                 weekly_earnings,
#                 monthly_earnings
#                 """
#             )
#             .eq("id", user_id)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     @staticmethod
#     def get_earnings(email: str):

#         response = (
#             supabase
#             .table("staff_earnings")
#             .select("AMOUNT, earned_at, payment_status")
#             .eq("staff_email", email)
#             .eq("payment_status", "paid")
#             .execute()
#         )

#         data = response.data or []

#         from datetime import datetime, timedelta, timezone

#         now = datetime.now(timezone.utc)
#         week_start = now - timedelta(days=7)

#         total = 0.0
#         weekly = 0.0
#         monthly = 0.0

#         for item in data:

#             amount = float(item.get("AMOUNT") or 0)

#             total += amount

#             earned_at = item.get("earned_at")

#             if not earned_at:
#                 continue

#             try:
#                 date = datetime.fromisoformat(
#                     earned_at.replace("Z", "+00:00")
#                 )

#                 # Make sure the datetime is timezone-aware.
#                 # Supabase/PostgreSQL may sometimes return a timestamp
#                 # without timezone information.
#                 if date.tzinfo is None:
#                     date = date.replace(tzinfo=timezone.utc)

#                 else:
#                     date = date.astimezone(timezone.utc)

#             except (ValueError, TypeError):
#                 continue

#             # Last 7 days
#             if date >= week_start:
#                 weekly += amount

#             # Current month
#             if (
#                 date.month == now.month
#                 and date.year == now.year
#             ):
#                 monthly += amount

#         return {
#             "total": total,
#             "weekly": weekly,
#             "monthly": monthly,
#         }









from datetime import datetime, timedelta, timezone

from app.supabase.client import supabase


class PartnerDashboardRepository:

    @staticmethod
    def get_booking_stats(email: str):

        new_response = (
            supabase
            .table("bookings")
            .select("id", count="exact")
            .eq("assigned_staff_email", email)
            .eq("is_viewed", False)
            .execute()
        )

        new_count = new_response.count or 0

        assigned_response = (
            supabase
            .table("bookings")
            .select("id", count="exact")
            .eq("assigned_staff_email", email)
            .eq("work_status", "ASSIGNED")
            .execute()
        )

        assigned_count = assigned_response.count or 0

        completed_response = (
            supabase
            .table("bookings")
            .select("id", count="exact")
            .eq("assigned_staff_email", email)
            .eq("work_status", "COMPLETED")
            .execute()
        )

        completed_count = completed_response.count or 0

        cancellation_response = (
            supabase
            .table("staff_cancellations")
            .select("id", count="exact")
            .eq("staff_email", email)
            .execute()
        )

        cancelled_count = cancellation_response.count or 0

        if cancelled_count == 0:

            cancelled_bookings = (
                supabase
                .table("bookings")
                .select("id", count="exact")
                .eq("assigned_staff_email", email)
                .eq("work_status", "CANCELLED")
                .execute()
            )

            cancelled_count = cancelled_bookings.count or 0

        return {
            "new": new_count,
            "assigned": assigned_count,
            "completed": completed_count,
            "cancelled": cancelled_count,
        }

    @staticmethod
    def get_profile(user_id: str):

        response = (
            supabase
            .table("staff_profile")
            .select(
                """
                id,
                email,
                is_available,
                is_blocked,
                today_duty_minutes,
                weekly_duty_minutes,
                monthly_duty_minutes,
                total_earnings,
                weekly_earnings,
                monthly_earnings
                """
            )
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    @staticmethod
    def get_earnings(email: str):

        response = (
            supabase
            .table("staff_earnings")
            .select(
                "AMOUNT, earned_at, payment_status"
            )
            .eq("staff_email", email)
            .eq("payment_status", "paid")
            .execute()
        )

        data = response.data or []

        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=7)

        total = 0.0
        weekly = 0.0
        monthly = 0.0

        for item in data:

            amount = float(
                item.get("AMOUNT") or 0
            )

            total += amount

            earned_at = item.get("earned_at")

            if not earned_at:
                continue

            try:

                date = datetime.fromisoformat(
                    earned_at.replace(
                        "Z",
                        "+00:00",
                    )
                )

                if date.tzinfo is None:
                    date = date.replace(
                        tzinfo=timezone.utc
                    )
                else:
                    date = date.astimezone(
                        timezone.utc
                    )

            except (ValueError, TypeError):
                continue

            if date >= week_start:
                weekly += amount

            if (
                date.month == now.month
                and date.year == now.year
            ):
                monthly += amount

        return {
            "total": total,
            "weekly": weekly,
            "monthly": monthly,
        }