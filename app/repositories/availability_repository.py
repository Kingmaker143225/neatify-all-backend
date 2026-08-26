# from app.supabase.client import supabase


# class AvailabilityRepository:

#     @staticmethod
#     def get_availability(
#         email: str,
#         month: str,
#     ):
#         profile_response = (
#             supabase
#             .from_("staff_profile")
#             .select("id, name, email")
#             .eq("email", email)
#             .maybe_single()
#             .execute()
#         )

#         profile = profile_response.data

#         if not profile:
#             return None

#         response = (
#             supabase
#             .from_("staff_monthly_availability")
#             .select("calendar_data")
#             .eq("staff_id", profile["id"])
#             .eq("month", month)
#             .maybe_single()
#             .execute()
#         )

#         data = response.data

#         return {
#             "staff_id": profile["id"],
#             "staff_name": profile.get("name"),
#             "staff_email": profile.get("email"),
#             "month": month,
#             "calendar_data": (
#                 data.get("calendar_data")
#                 if data
#                 else {}
#             ),
#         }

#     @staticmethod
#     def save_availability(
#         email: str,
#         month: str,
#         calendar_data: dict,
#     ):
#         profile_response = (
#             supabase
#             .from_("staff_profile")
#             .select("id, name, email")
#             .eq("email", email)
#             .maybe_single()
#             .execute()
#         )

#         profile = profile_response.data

#         if not profile:
#             return None

#         response = (
#             supabase
#             .from_("staff_monthly_availability")
#             .upsert(
#                 {
#                     "staff_id": profile["id"],
#                     "staff_name": profile.get("name"),
#                     "staff_email": profile.get("email"),
#                     "month": month,
#                     "calendar_data": calendar_data,
#                 },
#                 on_conflict="staff_id,month",
#             )
#             .execute()
#         )

#         return response.data















# from app.supabase.client import supabase


# class AvailabilityRepository:

#     @staticmethod
#     def get_availability(
#         email: str,
#         month: str,
#     ):
#         profile_response = (
#             supabase
#             .from_("staff_profile")
#             .select("id, name, email")
#             .eq("email", email)
#             .maybe_single()
#             .execute()
#         )

#         profile = profile_response.data

#         if not profile:
#             return None

#         availability_response = (
#             supabase
#             .from_("staff_monthly_availability")
#             .select("calendar_data")
#             .eq("staff_id", profile["id"])
#             .eq("month", month)
#             .maybe_single()
#             .execute()
#         )

#         availability = availability_response.data

#         return {
#             "staff_id": profile["id"],
#             "staff_name": profile.get("name"),
#             "staff_email": profile.get("email"),
#             "month": month,
#             "calendar_data": (
#                 availability.get("calendar_data")
#                 if availability
#                 else {}
#             ),
#         }

#     @staticmethod
#     def save_availability(
#         email: str,
#         month: str,
#         calendar_data: dict,
#     ):
#         profile_response = (
#             supabase
#             .from_("staff_profile")
#             .select("id, name, email")
#             .eq("email", email)
#             .maybe_single()
#             .execute()
#         )

#         profile = profile_response.data

#         if not profile:
#             return None

#         response = (
#             supabase
#             .from_("staff_monthly_availability")
#             .upsert(
#                 {
#                     "staff_id": profile["id"],
#                     "staff_name": profile.get("name"),
#                     "staff_email": profile.get("email"),
#                     "month": month,
#                     "calendar_data": calendar_data,
#                 },
#                 on_conflict="staff_id,month",
#             )
#             .execute()
#         )

#         return response.data















from app.supabase.client import supabase


class AvailabilityRepository:

    @staticmethod
    def get_availability(
        email: str,
        month: str,
    ):
        profile_response = (
            supabase
            .from_("staff_profile")
            .select("id, name, email")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        profile = profile_response.data

        if not profile:
            return None

        availability_response = (
            supabase
            .from_("staff_monthly_availability")
            .select("calendar_data")
            .eq("staff_id", profile["id"])
            .eq("month", month)
            .maybe_single()
            .execute()
        )

        # Handle case where no availability record exists
        availability = (
            availability_response.data
            if availability_response is not None
            else None
        )

        return {
            "staff_id": profile["id"],
            "staff_name": profile.get("name"),
            "staff_email": profile.get("email"),
            "month": month,
            "calendar_data": (
                availability.get("calendar_data")
                if availability
                else {}
            ),
        }

    @staticmethod
    def save_availability(
        email: str,
        month: str,
        calendar_data: dict,
    ):
        profile_response = (
            supabase
            .from_("staff_profile")
            .select("id, name, email")
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        profile = profile_response.data

        if not profile:
            return None

        response = (
            supabase
            .from_("staff_monthly_availability")
            .upsert(
                {
                    "staff_id": profile["id"],
                    "staff_name": profile.get("name"),
                    "staff_email": profile.get("email"),
                    "month": month,
                    "calendar_data": calendar_data,
                },
                on_conflict="staff_id,month",
            )
            .execute()
        )

        return response.data