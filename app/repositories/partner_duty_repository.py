# from datetime import datetime, timezone
# from typing import Any

# from app.supabase.client import supabase


# class PartnerDutyRepository:

#     @staticmethod
#     def get_staff_profile(user_id: str):
#         response = (
#             supabase
#             .table("staff_profile")
#             .select(
#                 """
#                 id,
#                 is_available,
#                 duty_started_at,
#                 duty_logs_json,
#                 duty_sessions_json
#                 """
#             )
#             .eq("id", user_id)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     @staticmethod
#     def update_duty_off(
#         user_id: str,
#         duty_logs: dict[str, int],
#         duty_sessions: list[dict[str, Any]],
#         today_minutes: int,
#         weekly_minutes: int,
#         monthly_minutes: int,
#     ):
#         response = (
#             supabase
#             .table("staff_profile")
#             .update(
#                 {
#                     "is_available": False,
#                     "is_out_of_zone": False,
#                     "work_start_location": None,
#                     "live_location": None,
#                     "live_location_updated_at": None,
#                     "duty_logs_json": duty_logs,
#                     "duty_sessions_json": duty_sessions,
#                     "today_duty_minutes": str(today_minutes),
#                     "weekly_duty_minutes": str(weekly_minutes),
#                     "monthly_duty_minutes": str(monthly_minutes),
#                     "push_token": None,
#                 }
#             )
#             .eq("id", user_id)
#             .execute()
#         )

#         return response.data









from datetime import datetime, timezone

from app.supabase.client import supabase


class PartnerDutyRepository:

    # =====================================================
    # GET PARTNER PROFILE
    # =====================================================

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
                duty_started_at,
                work_start_location,
                is_out_of_zone,
                live_location,
                live_location_updated_at,
                duty_logs_json,
                duty_sessions_json,
                today_duty_minutes,
                weekly_duty_minutes,
                monthly_duty_minutes
                """
            )
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =====================================================
    # TURN DUTY ON
    # =====================================================

    @staticmethod
    def turn_on_duty(
        user_id: str,
        duty_started_at: str,
        work_start_location=None,
    ):

        update_data = {
            "is_available": True,
            "is_out_of_zone": False,
            "duty_started_at": duty_started_at,
        }

        # Only update the location if one was supplied.
        if work_start_location is not None:
            update_data[
                "work_start_location"
            ] = work_start_location

        response = (
            supabase
            .table("staff_profile")
            .update(update_data)
            .eq("id", user_id)
            .execute()
        )

        return response.data

    # =====================================================
    # TURN DUTY OFF
    # =====================================================

    @staticmethod
    def turn_off_duty(
        user_id: str,
        duty_logs: dict,
        duty_sessions: list,
        today_minutes: int,
        weekly_minutes: int,
        monthly_minutes: int,
    ):

        response = (
            supabase
            .table("staff_profile")
            .update(
                {
                    "is_available": False,
                    "is_out_of_zone": False,
                    "work_start_location": None,
                    "live_location": None,
                    "live_location_updated_at": None,
                    "duty_started_at": None,
                    "duty_logs_json": duty_logs,
                    "duty_sessions_json": duty_sessions,
                    "today_duty_minutes": str(
                        today_minutes
                    ),
                    "weekly_duty_minutes": str(
                        weekly_minutes
                    ),
                    "monthly_duty_minutes": str(
                        monthly_minutes
                    ),
                    "push_token": None,
                }
            )
            .eq("id", user_id)
            .execute()
        )

        return response.data