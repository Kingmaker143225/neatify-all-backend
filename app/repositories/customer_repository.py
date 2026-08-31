# # from app.supabase.client import supabase


# # class CustomerRepository:

# #     # =========================================================
# #     # GET CUSTOMER PROFILE
# #     # =========================================================

# #     @staticmethod
# #     def get_profile(user_id: str):
# #         response = (
# #             supabase
# #             .table("profile")
# #             .select(
# #                 """
# #                 id,
# #                 full_name,
# #                 email,
# #                 phone
# #                 """
# #             )
# #             .eq("id", user_id)
# #             .maybe_single()
# #             .execute()
# #         )

# #         return response.data

# #     # =========================================================
# #     # CHECK CUSTOMER PROFILE EXISTS
# #     # =========================================================

# #     @staticmethod
# #     def profile_exists(user_id: str) -> bool:
# #         profile = (
# #             CustomerRepository
# #             .get_profile(user_id)
# #         )

# #         return profile is not None
    


# from app.supabase.client import supabase


# class CustomerRepository:

#     # =========================================================
#     # GET CUSTOMER PROFILE
#     # =========================================================

#     @staticmethod
#     def get_profile(user_id: str):
#         response = (
#             supabase
#             .table("profile")
#             .select(
#                 """
#                 id,
#                 full_name,
#                 email,
#                 phone,
#                 address,
#                 pincode
#                 """
#             )
#             .eq("id", user_id)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CREATE / UPDATE CUSTOMER PROFILE
#     # =========================================================

#     @staticmethod
#     def upsert_profile(
#         user_id: str,
#         full_name: str,
#         phone: str,
#         address: str,
#         pincode: str,
#         email: str,
#     ):
#         response = (
#             supabase
#             .table("profile")
#             .upsert(
#                 {
#                     "id": user_id,
#                     "full_name": full_name or None,
#                     "email": email or None,
#                     "phone": phone or None,
#                     "address": address or None,
#                     "pincode": pincode or None,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CHECK PROFILE EXISTS
#     # =========================================================

#     @staticmethod
#     def profile_exists(user_id: str) -> bool:
#         return (
#             CustomerRepository
#             .get_profile(user_id)
#             is not None
#         )













from app.supabase.client import supabase


class CustomerRepository:

    @staticmethod
    def get_profile(user_id: str):
        response = (
            supabase
            .table("profile")
            .select(
                """
                id,
                full_name,
                email,
                phone,
                address,
                pincode
                """
            )
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    @staticmethod
    def upsert_profile(
        user_id: str,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
        email: str,
    ):
        response = (
            supabase
            .table("profile")
            .upsert(
                {
                    "id": user_id,
                    "full_name": full_name or None,
                    "email": email or None,
                    "phone": phone or None,
                    "address": address or None,
                    "pincode": pincode or None,
                }
            )
            .execute()
        )

        return response.data

    @staticmethod
    def profile_exists(
        user_id: str,
    ) -> bool:
        return (
            CustomerRepository
            .get_profile(user_id)
            is not None
        )

    # =========================================================
    # GET CUSTOMER COUPON
    # =========================================================

    @staticmethod
    def get_customer_coupon(
        phone: str,
    ):
        response = (
            supabase
            .table("coupons")
            .select(
                """
                id,
                coupon_code,
                discount_percentage,
                discount_amount,
                phone_number,
                is_used,
                is_active,
                service_id
                """
            )
            .or_(
                f"phone_number.eq.{phone},"
                f"phone_number.eq.91{phone},"
                f"phone_number.eq.+91{phone}"
            )
            .eq("is_active", True)
            .eq("is_used", False)
            .order(
                "created_at",
                desc=True,
            )
            .limit(1)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # GET APP POLICIES
    # =========================================================

    @staticmethod
    def get_app_policies():
        response = (
            supabase
            .table("app_policies")
            .select(
                """
                user_policies,
                terms_and_conditions
                """
            )
            .eq("is_active", True)
            .limit(1)
            .maybe_single()
            .execute()
        )

        return response.data