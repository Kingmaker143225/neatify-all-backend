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













# from app.supabase.client import supabase


# class CustomerRepository:

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
#                 pincode,
#                 referral_code
#                 """
#             )
#             .eq("id", user_id)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     @staticmethod
#     def upsert_profile(
#         user_id: str,
#         full_name: str,
#         phone: str,
#         address: str,
#         pincode: str,
#         email: str,
#         referral_code: str | None = None,
#         referred_by_id: str | None = None,

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
#                     "referral_code": referral_code,
#                     "referred_by_id": referred_by_id,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     @staticmethod
#     def profile_exists(
#         user_id: str,
#     ) -> bool:
#         return (
#             CustomerRepository
#             .get_profile(user_id)
#             is not None
#         )

#     # =========================================================
#     # GET CUSTOMER COUPON
#     # =========================================================

#     @staticmethod
#     def get_customer_coupon(
#         phone: str,
#     ):
#         response = (
#             supabase
#             .table("coupons")
#             .select(
#                 """
#                 id,
#                 coupon_code,
#                 discount_percentage,
#                 discount_amount,
#                 phone_number,
#                 is_used,
#                 is_active,
#                 service_id
#                 """
#             )
#             .or_(
#                 f"phone_number.eq.{phone},"
#                 f"phone_number.eq.91{phone},"
#                 f"phone_number.eq.+91{phone}"
#             )
#             .eq("is_active", True)
#             .eq("is_used", False)
#             .order(
#                 "created_at",
#                 desc=True,
#             )
#             .limit(1)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # GET APP POLICIES
#     # =========================================================

#     @staticmethod
#     def get_app_policies():
#         response = (
#             supabase
#             .table("app_policies")
#             .select(
#                 """
#                 user_policies,
#                 terms_and_conditions
#                 """
#             )
#             .eq("is_active", True)
#             .limit(1)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

















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
#                 pincode,
#                 referral_code
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
#         referral_code: str | None = None,
#         referred_by_id: str | None = None,
#     ):
#         data = {
#             "id": user_id,
#             "full_name": full_name or None,
#             "email": email or None,
#             "phone": phone or None,
#             "address": address or None,
#             "pincode": pincode or None,
#         }

#         # Only update referral fields when explicitly supplied.
#         # This prevents normal profile updates from clearing
#         # an existing referral relationship.
#         if referral_code is not None:
#             data["referral_code"] = referral_code

#         if referred_by_id is not None:
#             data["referred_by_id"] = referred_by_id

#         response = (
#             supabase
#             .table("profile")
#             .upsert(data)
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CHECK PROFILE EXISTS
#     # =========================================================

#     @staticmethod
#     def profile_exists(
#         user_id: str,
#     ) -> bool:
#         return (
#             CustomerRepository
#             .get_profile(user_id)
#             is not None
#         )

#     # =========================================================
#     # GET REFERRER BY REFERRAL CODE
#     # =========================================================

#     @staticmethod
#     def get_referrer_by_code(
#         referral_code: str,
#     ):
#         response = (
#             supabase
#             .table("profile")
#             .select("id")
#             .eq(
#                 "referral_code",
#                 referral_code,
#             )
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPDATE SUPABASE AUTH USER
#     # =========================================================

#     @staticmethod
#     def update_auth_user(
#         user_id: str,
#         auth_payload: dict,
#     ):
#         return (
#             supabase
#             .auth
#             .admin
#             .update_user_by_id(
#                 user_id,
#                 auth_payload,
#             )
#         )

#     # =========================================================
#     # UPSERT SIGNUP
#     # =========================================================

#     @staticmethod
#     def upsert_signup(
#         user_id: str,
#         full_name: str,
#         email: str,
#         phone: str,
#     ):
#         response = (
#             supabase
#             .table("signup")
#             .upsert(
#                 {
#                     "id": user_id,
#                     "full_name": full_name,
#                     "email": email,
#                     "phone": phone,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPSERT WALLET
#     # =========================================================

#     @staticmethod
#     def upsert_wallet(
#         user_id: str,
#     ):
#         response = (
#             supabase
#             .table("wallet")
#             .upsert(
#                 {
#                     "user_id": user_id,
#                     "balance": 0,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CREATE REFERRAL
#     # =========================================================

#     @staticmethod
#     def create_referral(
#         referrer_id: str,
#         referred_user_id: str,
#     ):
#         response = (
#             supabase
#             .table("referrals")
#             .insert(
#                 {
#                     "referrer_id": referrer_id,
#                     "referred_user_id": referred_user_id,
#                     "status": "pending",
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # CREATE WELCOME COUPON
#     # =========================================================

#     @staticmethod
#     def create_welcome_coupon(
#         coupon_code: str,
#         phone: str,
#     ):
#         response = (
#             supabase
#             .table("coupons")
#             .insert(
#                 {
#                     "coupon_code": coupon_code,
#                     "discount_amount": 50,
#                     "is_used": False,
#                     "phone_number": phone,
#                 }
#             )
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # UPDATE WELCOME REWARD METADATA
#     # =========================================================

#     @staticmethod
#     def update_welcome_reward(
#         user_id: str,
#         coupon_code: str,
#     ):
#         try:
#             return (
#                 supabase
#                 .auth
#                 .admin
#                 .update_user_by_id(
#                     user_id,
#                     {
#                         "user_metadata": {
#                             "show_welcome_reward": True,
#                             "welcome_coupon_code": coupon_code,
#                         }
#                     },
#                 )
#             )
#         except Exception:
#             return None

#     # =========================================================
#     # GET CUSTOMER COUPON
#     # =========================================================

#     @staticmethod
#     def get_customer_coupon(
#         phone: str,
#     ):
#         response = (
#             supabase
#             .table("coupons")
#             .select(
#                 """
#                 id,
#                 coupon_code,
#                 discount_percentage,
#                 discount_amount,
#                 phone_number,
#                 is_used,
#                 is_active,
#                 service_id
#                 """
#             )
#             .or_(
#                 f"phone_number.eq.{phone},"
#                 f"phone_number.eq.91{phone},"
#                 f"phone_number.eq.+91{phone}"
#             )
#             .eq("is_active", True)
#             .eq("is_used", False)
#             .order(
#                 "created_at",
#                 desc=True,
#             )
#             .limit(1)
#             .maybe_single()
#             .execute()
#         )

#         return response.data

#     # =========================================================
#     # GET APP POLICIES
#     # =========================================================

#     @staticmethod
#     def get_app_policies():
#         response = (
#             supabase
#             .table("app_policies")
#             .select(
#                 """
#                 user_policies,
#                 terms_and_conditions
#                 """
#             )
#             .eq("is_active", True)
#             .limit(1)
#             .maybe_single()
#             .execute()
#         )

#         return response.data























from app.supabase.client import supabase


class CustomerRepository:

    # =========================================================
    # GET CUSTOMER PROFILE
    # =========================================================

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
                pincode,
                referral_code
                """
            )
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # CREATE / UPDATE CUSTOMER PROFILE
    # =========================================================

    @staticmethod
    def upsert_profile(
        user_id: str,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
        email: str,
        referral_code: str | None = None,
        referred_by_id: str | None = None,
    ):
        data = {
            "id": user_id,
            "full_name": full_name or None,
            "email": email or None,
            "phone": phone or None,
            "address": address or None,
            "pincode": pincode or None,
        }

        # Only update referral fields when explicitly supplied.
        # This prevents normal profile updates from clearing
        # an existing referral relationship.
        if referral_code is not None:
            data["referral_code"] = referral_code

        if referred_by_id is not None:
            data["referred_by_id"] = referred_by_id

        response = (
            supabase
            .table("profile")
            .upsert(data)
            .execute()
        )

        return response.data

    # =========================================================
    # CHECK PROFILE EXISTS
    # =========================================================

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
    # GET REFERRER BY REFERRAL CODE
    # =========================================================

    @staticmethod
    def get_referrer_by_code(
        referral_code: str,
    ):
        response = (
            supabase
            .table("profile")
            .select("id")
            .eq(
                "referral_code",
                referral_code,
            )
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # UPDATE SUPABASE AUTH USER
    # =========================================================

    @staticmethod
    def update_auth_user(
        user_id: str,
        auth_payload: dict,
    ):
        return (
            supabase
            .auth
            .admin
            .update_user_by_id(
                user_id,
                auth_payload,
            )
        )

    # =========================================================
    # UPSERT SIGNUP
    # =========================================================

    @staticmethod
    def upsert_signup(
        user_id: str,
        full_name: str,
        email: str,
        phone: str,
    ):
        response = (
            supabase
            .table("signup")
            .upsert(
                {
                    "id": user_id,
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                }
            )
            .execute()
        )

        return response.data

    # =========================================================
    # UPSERT WALLET
    # =========================================================

    @staticmethod
    def upsert_wallet(
        user_id: str,
    ):
        response = (
            supabase
            .table("wallet")
            .upsert(
                {
                    "user_id": user_id,
                    "balance": 0,
                }
            )
            .execute()
        )

        return response.data

    # =========================================================
    # CREATE REFERRAL
    # =========================================================

    @staticmethod
    def create_referral(
        referrer_id: str,
        referred_user_id: str,
    ):
        response = (
            supabase
            .table("referrals")
            .insert(
                {
                    "referrer_id": referrer_id,
                    "referred_user_id": referred_user_id,
                    "status": "pending",
                }
            )
            .execute()
        )

        return response.data

    # =========================================================
    # CREATE WELCOME COUPON
    # =========================================================

    @staticmethod
    def create_welcome_coupon(
        coupon_code: str,
        phone: str,
    ):
        response = (
            supabase
            .table("coupons")
            .insert(
                {
                    "coupon_code": coupon_code,
                    "discount_amount": 50,
                    "is_used": False,
                    "phone_number": phone,
                }
            )
            .execute()
        )

        return response.data

    # =========================================================
    # UPDATE WELCOME REWARD METADATA
    # =========================================================

    @staticmethod
    def update_welcome_reward(
        user_id: str,
        coupon_code: str,
    ):
        try:
            return (
                supabase
                .auth
                .admin
                .update_user_by_id(
                    user_id,
                    {
                        "user_metadata": {
                            "show_welcome_reward": True,
                            "welcome_coupon_code": coupon_code,
                        }
                    },
                )
            )
        except Exception:
            return None

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

    # =========================================================
    # ✅ GET USER BY EMAIL (NEW - For Google OAuth)
    # =========================================================

    @staticmethod
    def get_user_by_email(email: str):
        """
        Find a user by email in the profile table.
        Used for Google OAuth to check if a user already exists.
        """
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
                pincode,
                referral_code
                """
            )
            .eq("email", email)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # ✅ GET USER BY PHONE (NEW - For Google OAuth)
    # =========================================================

    @staticmethod
    def get_user_by_phone(phone: str):
        """
        Find a user by phone number in the profile table.
        Used for Google OAuth to check if a user already exists.
        """
        # Clean phone to 10 digits
        clean_phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )[-10:]

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
                pincode,
                referral_code
                """
            )
            .eq("phone", clean_phone)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # ✅ CREATE OR GET USER FROM GOOGLE OAUTH (NEW)
    # =========================================================

    @staticmethod
    def find_or_create_google_user(
        email: str,
        full_name: str,
        phone: str | None = None,
    ) -> dict:
        """
        Find an existing user by email or create a new one for Google OAuth.
        Returns the user profile.
        """
        # 1. Try to find user by email
        user = CustomerRepository.get_user_by_email(email)
        
        if user:
            return user
        
        # 2. Try to find user by phone (if provided)
        if phone:
            user = CustomerRepository.get_user_by_phone(phone)
            if user:
                # Update email if phone exists but email is different
                CustomerRepository.upsert_profile(
                    user_id=user["id"],
                    full_name=user.get("full_name", full_name),
                    phone=user.get("phone", phone),
                    address=user.get("address", ""),
                    pincode=user.get("pincode", ""),
                    email=email,
                )
                # Get updated profile
                return CustomerRepository.get_profile(user["id"])
        
        # 3. Create new user
        # Generate a UUID for the new user
        import uuid
        user_id = str(uuid.uuid4())
        
        # Create auth user first (via Supabase Auth)
        # This will be handled in the service layer
        
        return None