# from datetime import datetime, timedelta, timezone
# from typing import Any

# from fastapi import HTTPException, status

# from app.repositories.partner_duty_repository import (
#     PartnerDutyRepository,
# )


# class PartnerDutyService:

#     # =====================================================
#     # DATE/TIME HELPERS
#     # =====================================================

#     @staticmethod
#     def parse_datetime(value: str | datetime | None):
#         if value is None:
#             return None

#         if isinstance(value, datetime):
#             dt = value
#         else:
#             dt = datetime.fromisoformat(
#                 value.replace("Z", "+00:00")
#             )

#         # Always work with timezone-aware UTC datetimes.
#         if dt.tzinfo is None:
#             dt = dt.replace(tzinfo=timezone.utc)
#         else:
#             dt = dt.astimezone(timezone.utc)

#         return dt

#     # =====================================================
#     # SPLIT SESSION ACROSS MIDNIGHT
#     # =====================================================

#     @staticmethod
#     def split_and_add_session_logs(
#         existing_logs: dict[str, int],
#         started_at: datetime,
#         ended_at: datetime,
#     ) -> dict[str, int]:

#         updated_logs = dict(existing_logs or {})

#         if ended_at <= started_at:
#             return updated_logs

#         current_cursor = started_at

#         while current_cursor < ended_at:

#             current_day_key = (
#                 current_cursor.strftime("%Y-%m-%d")
#             )

#             # End of current UTC day.
#             next_day = (
#                 current_cursor
#                 .replace(
#                     hour=0,
#                     minute=0,
#                     second=0,
#                     microsecond=0,
#                 )
#                 + timedelta(days=1)
#             )

#             chunk_end = min(
#                 ended_at,
#                 next_day,
#             )

#             chunk_seconds = (
#                 chunk_end - current_cursor
#             ).total_seconds()

#             chunk_minutes = max(
#                 0,
#                 int(chunk_seconds // 60),
#             )

#             if chunk_minutes > 0:

#                 previous_minutes = int(
#                     updated_logs.get(
#                         current_day_key,
#                         0,
#                     )
#                     or 0
#                 )

#                 updated_logs[
#                     current_day_key
#                 ] = (
#                     previous_minutes
#                     + chunk_minutes
#                 )

#             current_cursor = next_day

#         return updated_logs

#     # =====================================================
#     # CALCULATE DUTY TOTALS
#     # =====================================================

#     @staticmethod
#     def calculate_duty_totals(
#         logs: dict[str, int],
#     ) -> dict[str, int]:

#         now = datetime.now(timezone.utc)

#         today_key = now.strftime(
#             "%Y-%m-%d"
#         )

#         month_key = now.strftime(
#             "%Y-%m"
#         )

#         # Monday = 0
#         days_since_monday = now.weekday()

#         start_of_week = (
#             now
#             - timedelta(
#                 days=days_since_monday
#             )
#         ).replace(
#             hour=0,
#             minute=0,
#             second=0,
#             microsecond=0,
#         )

#         end_of_week = (
#             start_of_week
#             + timedelta(days=7)
#         )

#         today_base = int(
#             logs.get(today_key, 0)
#             or 0
#         )

#         weekly_base = 0
#         monthly_base = 0

#         for date_string, minutes in logs.items():

#             try:
#                 date_value = datetime.strptime(
#                     date_string,
#                     "%Y-%m-%d",
#                 ).replace(
#                     tzinfo=timezone.utc
#                 )

#             except (ValueError, TypeError):
#                 continue

#             minute_value = int(
#                 minutes or 0
#             )

#             # Weekly
#             if (
#                 start_of_week
#                 <= date_value
#                 < end_of_week
#             ):
#                 weekly_base += minute_value

#             # Monthly
#             if date_string.startswith(
#                 month_key
#             ):
#                 monthly_base += minute_value

#         return {
#             "today": today_base,
#             "weekly": weekly_base,
#             "monthly": monthly_base,
#         }

#     # =====================================================
#     # DUTY OFF
#     # =====================================================

#     @staticmethod
#     def turn_off_duty(
#         user_id: str,
#     ):

#         # -------------------------------------------------
#         # Get current partner profile
#         # -------------------------------------------------

#         profile = (
#             PartnerDutyRepository
#             .get_staff_profile(
#                 user_id
#             )
#         )

#         if not profile:

#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Partner profile not found.",
#             )

#         # -------------------------------------------------
#         # Existing duty logs
#         # -------------------------------------------------

#         existing_logs = (
#             profile.get(
#                 "duty_logs_json"
#             )
#             or {}
#         )

#         if not isinstance(
#             existing_logs,
#             dict,
#         ):
#             existing_logs = {}

#         updated_logs = dict(
#             existing_logs
#         )

#         # -------------------------------------------------
#         # Existing duty sessions
#         # -------------------------------------------------

#         existing_sessions = (
#             profile.get(
#                 "duty_sessions_json"
#             )
#             or []
#         )

#         if not isinstance(
#             existing_sessions,
#             list,
#         ):
#             existing_sessions = []

#         updated_sessions = list(
#             existing_sessions
#         )

#         # -------------------------------------------------
#         # Finalize active duty session
#         # -------------------------------------------------

#         duty_started_at = (
#             profile.get(
#                 "duty_started_at"
#             )
#         )

#         now = datetime.now(
#             timezone.utc
#         )

#         if duty_started_at:

#             active_started_at = (
#                 PartnerDutyService
#                 .parse_datetime(
#                     duty_started_at
#                 )
#             )

#             if active_started_at:

#                 total_session_minutes = max(
#                     0,
#                     int(
#                         (
#                             now
#                             - active_started_at
#                         ).total_seconds()
#                         // 60
#                     ),
#                 )

#                 # -----------------------------------------
#                 # Add session time to daily logs
#                 # -----------------------------------------

#                 updated_logs = (
#                     PartnerDutyService
#                     .split_and_add_session_logs(
#                         updated_logs,
#                         active_started_at,
#                         now,
#                     )
#                 )

#                 # -----------------------------------------
#                 # Close currently open session
#                 # -----------------------------------------

#                 found_active = False

#                 for session in updated_sessions:

#                     if not isinstance(
#                         session,
#                         dict,
#                     ):
#                         continue

#                     if not session.get(
#                         "off_at"
#                     ):

#                         found_active = True

#                         session[
#                             "off_at"
#                         ] = now.isoformat()

#                         session[
#                             "duration_minutes"
#                         ] = (
#                             total_session_minutes
#                         )

#                 # -----------------------------------------
#                 # If no active session exists,
#                 # create one.
#                 # -----------------------------------------

#                 if not found_active:

#                     updated_sessions.append(
#                         {
#                             "id": (
#                                 f"sess_"
#                                 f"{int(now.timestamp() * 1000)}"
#                             ),
#                             "date": (
#                                 active_started_at
#                                 .strftime(
#                                     "%Y-%m-%d"
#                                 )
#                             ),
#                             "on_at": (
#                                 active_started_at
#                                 .isoformat()
#                             ),
#                             "off_at": (
#                                 now.isoformat()
#                             ),
#                             "location": None,
#                             "duration_minutes": (
#                                 total_session_minutes
#                             ),
#                         }
#                     )

#         # -------------------------------------------------
#         # Calculate final totals
#         # -------------------------------------------------

#         totals = (
#             PartnerDutyService
#             .calculate_duty_totals(
#                 updated_logs
#             )
#         )

#         # -------------------------------------------------
#         # Update Supabase
#         # -------------------------------------------------

#         updated = (
#             PartnerDutyRepository
#             .update_duty_off(
#                 user_id=user_id,
#                 duty_logs=updated_logs,
#                 duty_sessions=updated_sessions,
#                 today_minutes=totals[
#                     "today"
#                 ],
#                 weekly_minutes=totals[
#                     "weekly"
#                 ],
#                 monthly_minutes=totals[
#                     "monthly"
#                 ],
#             )
#         )

#         return {
#             "success": True,
#             "message": "Duty turned off successfully.",
#             "duty": {
#                 "is_available": False,
#                 "today_minutes": totals[
#                     "today"
#                 ],
#                 "weekly_minutes": totals[
#                     "weekly"
#                 ],
#                 "monthly_minutes": totals[
#                     "monthly"
#                 ],
#             },
#             "data": updated,
#         }








from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status

from app.repositories.partner_duty_repository import (
    PartnerDutyRepository,
)


class PartnerDutyService:

    # =====================================================
    # DATETIME HELPER
    # =====================================================

    @staticmethod
    def parse_datetime(
        value: str | datetime | None,
    ):

        if value is None:
            return None

        if isinstance(value, datetime):
            dt = value
        else:
            dt = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=timezone.utc
            )
        else:
            dt = dt.astimezone(
                timezone.utc
            )

        return dt

    # =====================================================
    # DUTY ON
    # =====================================================

    @staticmethod
    def turn_on_duty(
        user_id: str,
        work_start_location=None,
    ):

        # -------------------------------------------------
        # 1. Get partner profile
        # -------------------------------------------------

        profile = (
            PartnerDutyRepository
            .get_profile(user_id)
        )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner profile not found.",
            )

        # -------------------------------------------------
        # 2. Check blocked status
        # -------------------------------------------------

        if profile.get("is_blocked") is True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your partner account is blocked.",
            )

        # -------------------------------------------------
        # 3. Already on duty
        # -------------------------------------------------

        if profile.get("is_available") is True:
            return {
                "success": True,
                "message": "You are already on duty.",
                "duty": {
                    "is_available": True,
                    "duty_started_at": profile.get(
                        "duty_started_at"
                    ),
                },
            }

        # -------------------------------------------------
        # 4. Current UTC time
        # -------------------------------------------------

        now = datetime.now(timezone.utc)

        duty_started_at = now.isoformat()

        # -------------------------------------------------
        # 5. Update Supabase through Repository
        # -------------------------------------------------

        updated = (
            PartnerDutyRepository
            .turn_on_duty(
                user_id=user_id,
                duty_started_at=duty_started_at,
                work_start_location=work_start_location,
            )
        )

        # -------------------------------------------------
        # 6. Verify database update
        # -------------------------------------------------

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update partner duty status.",
            )

        # -------------------------------------------------
        # 7. Success
        # -------------------------------------------------

        return {
            "success": True,
            "message": "Duty started successfully.",
            "duty": {
                "is_available": True,
                "duty_started_at": duty_started_at,
            },
            "data": updated,
        }
    # =====================================================
    # SPLIT SESSION ACROSS MIDNIGHT
    # =====================================================

    @staticmethod
    def split_and_add_session_logs(
        existing_logs: dict[str, int],
        started_at: datetime,
        ended_at: datetime,
    ):

        updated_logs = dict(
            existing_logs or {}
        )

        if ended_at <= started_at:
            return updated_logs

        current_cursor = started_at

        while current_cursor < ended_at:

            current_day_key = (
                current_cursor.strftime(
                    "%Y-%m-%d"
                )
            )

            next_day = (
                current_cursor
                .replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                + timedelta(days=1)
            )

            chunk_end = min(
                ended_at,
                next_day,
            )

            chunk_seconds = (
                chunk_end - current_cursor
            ).total_seconds()

            chunk_minutes = max(
                0,
                int(
                    chunk_seconds // 60
                ),
            )

            if chunk_minutes > 0:

                previous_minutes = int(
                    updated_logs.get(
                        current_day_key,
                        0,
                    )
                    or 0
                )

                updated_logs[
                    current_day_key
                ] = (
                    previous_minutes
                    + chunk_minutes
                )

            current_cursor = next_day

        return updated_logs

    # =====================================================
    # CALCULATE TOTALS
    # =====================================================

    @staticmethod
    def calculate_duty_totals(
        logs: dict[str, int],
    ):

        now = datetime.now(
            timezone.utc
        )

        today_key = now.strftime(
            "%Y-%m-%d"
        )

        month_key = now.strftime(
            "%Y-%m"
        )

        days_since_monday = (
            now.weekday()
        )

        start_of_week = (
            now
            - timedelta(
                days=days_since_monday
            )
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        end_of_week = (
            start_of_week
            + timedelta(days=7)
        )

        today_base = int(
            logs.get(
                today_key,
                0,
            )
            or 0
        )

        weekly_base = 0
        monthly_base = 0

        for date_string, minutes in logs.items():

            try:
                date_value = (
                    datetime.strptime(
                        date_string,
                        "%Y-%m-%d",
                    ).replace(
                        tzinfo=timezone.utc
                    )
                )

            except (
                ValueError,
                TypeError,
            ):
                continue

            minute_value = int(
                minutes or 0
            )

            if (
                start_of_week
                <= date_value
                < end_of_week
            ):
                weekly_base += minute_value

            if date_string.startswith(
                month_key
            ):
                monthly_base += minute_value

        return {
            "today": today_base,
            "weekly": weekly_base,
            "monthly": monthly_base,
        }

    # =====================================================
    # DUTY OFF
    # =====================================================

    @staticmethod
    def turn_off_duty(
        user_id: str,
    ):

        profile = (
            PartnerDutyRepository
            .get_profile(user_id)
        )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner profile not found.",
            )

        # -------------------------------------------------
        # Existing logs
        # -------------------------------------------------

        existing_logs = (
            profile.get(
                "duty_logs_json"
            )
            or {}
        )

        if not isinstance(
            existing_logs,
            dict,
        ):
            existing_logs = {}

        updated_logs = dict(
            existing_logs
        )

        # -------------------------------------------------
        # Existing sessions
        # -------------------------------------------------

        existing_sessions = (
            profile.get(
                "duty_sessions_json"
            )
            or []
        )

        if not isinstance(
            existing_sessions,
            list,
        ):
            existing_sessions = []

        updated_sessions = list(
            existing_sessions
        )

        # -------------------------------------------------
        # Active duty
        # -------------------------------------------------

        duty_started_at = (
            profile.get(
                "duty_started_at"
            )
        )

        now = datetime.now(
            timezone.utc
        )

        if duty_started_at:

            active_started_at = (
                PartnerDutyService
                .parse_datetime(
                    duty_started_at
                )
            )

            if active_started_at:

                total_session_minutes = max(
                    0,
                    int(
                        (
                            now
                            - active_started_at
                        ).total_seconds()
                        // 60
                    ),
                )

                # -----------------------------------------
                # Add time to daily logs
                # -----------------------------------------

                updated_logs = (
                    PartnerDutyService
                    .split_and_add_session_logs(
                        updated_logs,
                        active_started_at,
                        now,
                    )
                )

                # -----------------------------------------
                # Close active session
                # -----------------------------------------

                found_active = False

                for session in updated_sessions:

                    if not isinstance(
                        session,
                        dict,
                    ):
                        continue

                    if not session.get(
                        "off_at"
                    ):

                        found_active = True

                        session[
                            "off_at"
                        ] = now.isoformat()

                        session[
                            "duration_minutes"
                        ] = (
                            total_session_minutes
                        )

                # -----------------------------------------
                # Create session if missing
                # -----------------------------------------

                if not found_active:

                    updated_sessions.append(
                        {
                            "id": (
                                f"sess_"
                                f"{int(now.timestamp() * 1000)}"
                            ),
                            "date": (
                                active_started_at
                                .strftime(
                                    "%Y-%m-%d"
                                )
                            ),
                            "on_at": (
                                active_started_at
                                .isoformat()
                            ),
                            "off_at": (
                                now.isoformat()
                            ),
                            "location": None,
                            "duration_minutes": (
                                total_session_minutes
                            ),
                        }
                    )

        # -------------------------------------------------
        # Calculate totals
        # -------------------------------------------------

        totals = (
            PartnerDutyService
            .calculate_duty_totals(
                updated_logs
            )
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        updated = (
            PartnerDutyRepository
            .turn_off_duty(
                user_id=user_id,
                duty_logs=updated_logs,
                duty_sessions=updated_sessions,
                today_minutes=totals[
                    "today"
                ],
                weekly_minutes=totals[
                    "weekly"
                ],
                monthly_minutes=totals[
                    "monthly"
                ],
            )
        )

        return {
            "success": True,
            "message": "Duty turned off successfully.",
            "duty": {
                "is_available": False,
                "today_minutes": totals[
                    "today"
                ],
                "weekly_minutes": totals[
                    "weekly"
                ],
                "monthly_minutes": totals[
                    "monthly"
                ],
            },
            "data": updated,
        }