# from fastapi import HTTPException, status

# from app.repositories.customer_repository import (
#     CustomerRepository,
# )
# import random
# import string

# from app.supabase.client import supabase


# class CustomerProfileService:

#     # =========================================================
#     # GET PROFILE
#     # =========================================================

#     @staticmethod
#     def get_profile(
#         customer,
#     ):
#         user = customer["user"]
#         user_id = str(user.id)

#         profile = (
#             CustomerRepository
#             .get_profile(user_id)
#         )

#         # -----------------------------------------------------
#         # PROFILE DOES NOT EXIST
#         # -----------------------------------------------------

#         if not profile:
#             return {
#                 "id": user_id,
#                 "full_name": None,
#                 "email": user.email or "",
#                 "phone": None,
#                 "address": None,
#                 "pincode": None,
#                 "referral_code": None,
#             }

#         # -----------------------------------------------------
#         # AUTH EMAIL IS THE SOURCE OF TRUTH
#         # -----------------------------------------------------

#         return {
#             "id": user_id,
#             "full_name": profile.get("full_name"),
#             "email": (
#                 user.email
#                 or profile.get("email")
#                 or ""
#             ),
#             "phone": profile.get("phone"),
#             "address": profile.get("address"),
#             "pincode": profile.get("pincode"),
#             "referral_code": profile.get("referral_code"),
#         }

#     # =========================================================
#     # UPDATE PROFILE
#     # =========================================================

#     @staticmethod
#     def update_profile(
#         customer,
#         full_name: str,
#         phone: str,
#         address: str,
#         pincode: str,
        
#     ):
#         user = customer["user"]
#         user_id = str(user.id)

#         # -----------------------------------------------------
#         # CLEAN PHONE
#         # -----------------------------------------------------

#         clean_phone = "".join(
#             character
#             for character in phone
#             if character.isdigit()
#         )

#         if len(clean_phone) != 10:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=(
#                     "Phone number must be exactly "
#                     "10 digits."
#                 ),
#             )

#         # -----------------------------------------------------
#         # CLEAN DATA
#         # -----------------------------------------------------

#         clean_name = full_name.strip()
#         clean_address = address.strip()
#         clean_pincode = pincode.strip()

#         if not clean_name:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Full name is required.",
#             )

#         # -----------------------------------------------------
#         # AUTH EMAIL
#         # -----------------------------------------------------

#         email = user.email or ""

#         # -----------------------------------------------------
#         # UPSERT PROFILE
#         # -----------------------------------------------------

#         CustomerRepository.upsert_profile(
#             user_id=user_id,
#             full_name=clean_name,
#             phone=clean_phone,
#             address=clean_address,
#             pincode=clean_pincode,
#             email=email,
#         )

#         # -----------------------------------------------------
#         # RETURN UPDATED PROFILE
#         # -----------------------------------------------------

#         return (
#             CustomerProfileService
#             .get_profile(
#                 customer=customer,
#             )
#         )

#         # =========================================================
#     # COMPLETE PROFILE
#     # =========================================================

#     @staticmethod
#     def complete_profile(
#         customer,
#         full_name: str,
#         email: str,
#         phone: str,
#         password: str | None = None,
#         referral_code: str | None = None,
#     ):
#         user = customer["user"]
#         user_id = str(user.id)

#         # -----------------------------------------------------
#         # CLEAN DATA
#         # -----------------------------------------------------

#         clean_name = full_name.strip()
#         clean_email = email.strip()
#         clean_phone = "".join(
#             character
#             for character in phone
#             if character.isdigit()
#         )[-10:]

#         if not clean_name:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Full name is required.",
#             )

#         if len(clean_phone) != 10:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Phone number must be exactly 10 digits.",
#             )

#         if not clean_email:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Email is required.",
#             )

#         # -----------------------------------------------------
#         # REFERRAL
#         # -----------------------------------------------------

#         referrer_id = None

#         if referral_code and referral_code.strip():

#             referral = (
#                 supabase
#                 .table("profile")
#                 .select("id")
#                 .eq(
#                     "referral_code",
#                     referral_code.strip().upper(),
#                 )
#                 .maybe_single()
#                 .execute()
#             )

#             if not referral.data:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Invalid referral code.",
#                 )

#             referrer_id = referral.data["id"]

#             # Prevent self-referral
#             if str(referrer_id) == user_id:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="You cannot use your own referral code.",
#                 )

#         # -----------------------------------------------------
#         # GENERATE THIS CUSTOMER'S OWN REFERRAL CODE
#         # -----------------------------------------------------

#         existing_profile = (
#             CustomerRepository
#             .get_profile(user_id)
#         )

#         my_referral_code = (
#             existing_profile.get("referral_code")
#             if existing_profile
#             else None
#         )

#         if not my_referral_code:
#             prefix = (
#                 "".join(
#                     character
#                     for character in clean_name.upper()
#                     if character.isalnum()
#                 )[:3]
#                 or "USR"
#             )

#             suffix = "".join(
#                 random.choices(
#                     string.ascii_uppercase
#                     + string.digits,
#                     k=6,
#                 )
#             )

#             my_referral_code = (
#                 f"NEAT-{prefix}{suffix}"
#             )

#         # -----------------------------------------------------
#         # UPDATE SUPABASE AUTH USER
#         # -----------------------------------------------------

#         auth_payload = {
#             "user_metadata": {
#                 "full_name": clean_name,
#                 "phone_number": f"+91{clean_phone}",
#             }
#         }

#         if password:
#             auth_payload["password"] = password

#         if clean_email != (user.email or ""):
#             auth_payload["email"] = clean_email

#         try:
#             supabase.auth.admin.update_user_by_id(
#                 user_id,
#                 auth_payload,
#             )
#         except Exception as exc:
#             raise HTTPException(
#                 status_code=400,
#                 detail=str(exc),
#             ) from exc

#         # -----------------------------------------------------
#         # PROFILE
#         # -----------------------------------------------------

#         CustomerRepository.upsert_profile(
#             user_id=user_id,
#             full_name=clean_name,
#             phone=clean_phone,
#             address=(
#                 existing_profile.get("address")
#                 if existing_profile
#                 else ""
#             ),
#             pincode=(
#                 existing_profile.get("pincode")
#                 if existing_profile
#                 else ""
#             ),
#             email=clean_email,
#             referral_code=my_referral_code,
#             referred_by_id=referrer_id,
#         )

#         # -----------------------------------------------------
#         # SIGNUP TABLE
#         # -----------------------------------------------------

#         (
#             supabase
#             .table("signup")
#             .upsert(
#                 {
#                     "id": user_id,
#                     "full_name": clean_name,
#                     "email": clean_email,
#                     "phone": clean_phone,
#                 }
#             )
#             .execute()
#         )

#         # -----------------------------------------------------
#         # WALLET
#         # -----------------------------------------------------

#         (
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

#         # -----------------------------------------------------
#         # REFERRAL TRACKING + WELCOME COUPON
#         # -----------------------------------------------------

#         welcome_coupon_code = None

#         if referrer_id:

#             (
#                 supabase
#                 .table("referrals")
#                 .insert(
#                     {
#                         "referrer_id": referrer_id,
#                         "referred_user_id": user_id,
#                         "status": "pending",
#                     }
#                 )
#                 .execute()
#             )

#             welcome_coupon_code = (
#                 "WELCOME50_"
#                 + "".join(
#                     random.choices(
#                         string.ascii_uppercase
#                         + string.digits,
#                         k=4,
#                     )
#                 )
#             )

#             (
#                 supabase
#                 .table("coupons")
#                 .insert(
#                     {
#                         "coupon_code": welcome_coupon_code,
#                         "discount_amount": 50,
#                         "is_used": False,
#                         "phone_number": clean_phone,
#                     }
#                 )
#                 .execute()
#             )

#             # -------------------------------------------------
#             # AUTH METADATA
#             # -------------------------------------------------

#             try:
#                 supabase.auth.admin.update_user_by_id(
#                     user_id,
#                     {
#                         "user_metadata": {
#                             "show_welcome_reward": True,
#                             "welcome_coupon_code": (
#                                 welcome_coupon_code
#                             ),
#                         }
#                     },
#                 )
#             except Exception:
#                 pass

#         # -----------------------------------------------------
#         # RETURN COMPLETE PROFILE
#         # -----------------------------------------------------

#         return CustomerProfileService.get_profile(
#             customer=customer,
#         )
























from fastapi import HTTPException, status

from app.repositories.customer_repository import (
    CustomerRepository,
)

import random
import string


class CustomerProfileService:

    # =========================================================
    # GET PROFILE
    # =========================================================

    @staticmethod
    def get_profile(
        customer,
    ):
        user = customer["user"]
        user_id = str(user.id)

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        # -----------------------------------------------------
        # PROFILE DOES NOT EXIST
        # -----------------------------------------------------

        if not profile:
            return {
                "id": user_id,
                "full_name": None,
                "email": user.email or "",
                "phone": None,
                "address": None,
                "pincode": None,
                "referral_code": None,
            }

        # -----------------------------------------------------
        # AUTH EMAIL IS THE SOURCE OF TRUTH
        # -----------------------------------------------------

        return {
            "id": user_id,
            "full_name": profile.get("full_name"),
            "email": (
                user.email
                or profile.get("email")
                or ""
            ),
            "phone": profile.get("phone"),
            "address": profile.get("address"),
            "pincode": profile.get("pincode"),
            "referral_code": profile.get("referral_code"),
        }

    # =========================================================
    # UPDATE PROFILE
    # =========================================================

    @staticmethod
    def update_profile(
        customer,
        full_name: str,
        phone: str,
        address: str,
        pincode: str,
    ):
        user = customer["user"]
        user_id = str(user.id)

        # -----------------------------------------------------
        # CLEAN PHONE
        # -----------------------------------------------------

        clean_phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Phone number must be exactly "
                    "10 digits."
                ),
            )

        # -----------------------------------------------------
        # CLEAN DATA
        # -----------------------------------------------------

        clean_name = full_name.strip()
        clean_address = address.strip()
        clean_pincode = pincode.strip()

        if not clean_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name is required.",
            )

        # -----------------------------------------------------
        # AUTH EMAIL
        # -----------------------------------------------------

        email = user.email or ""

        # -----------------------------------------------------
        # UPSERT PROFILE
        # -----------------------------------------------------

        CustomerRepository.upsert_profile(
            user_id=user_id,
            full_name=clean_name,
            phone=clean_phone,
            address=clean_address,
            pincode=clean_pincode,
            email=email,
        )

        # -----------------------------------------------------
        # RETURN UPDATED PROFILE
        # -----------------------------------------------------

        return (
            CustomerProfileService
            .get_profile(
                customer=customer,
            )
        )

    # =========================================================
    # COMPLETE PROFILE
    # =========================================================

    @staticmethod
    def complete_profile(
        customer,
        full_name: str,
        email: str,
        phone: str,
        password: str | None = None,
        referral_code: str | None = None,
    ):
        user = customer["user"]
        user_id = str(user.id)

        # -----------------------------------------------------
        # CLEAN DATA
        # -----------------------------------------------------

        clean_name = full_name.strip()
        clean_email = email.strip()

        clean_phone = "".join(
            character
            for character in phone
            if character.isdigit()
        )[-10:]

        if not clean_name:
            raise HTTPException(
                status_code=400,
                detail="Full name is required.",
            )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=400,
                detail="Phone number must be exactly 10 digits.",
            )

        if not clean_email:
            raise HTTPException(
                status_code=400,
                detail="Email is required.",
            )

        # -----------------------------------------------------
        # REFERRAL
        # -----------------------------------------------------

        referrer_id = None

        if referral_code and referral_code.strip():

            referral = (
                CustomerRepository
                .get_referrer_by_code(
                    referral_code.strip().upper()
                )
            )

            if not referral:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid referral code.",
                )

            referrer_id = referral["id"]

            # Prevent self-referral
            if str(referrer_id) == user_id:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "You cannot use your own referral code."
                    ),
                )

        # -----------------------------------------------------
        # GET EXISTING PROFILE
        # -----------------------------------------------------

        existing_profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        # -----------------------------------------------------
        # GENERATE THIS CUSTOMER'S OWN REFERRAL CODE
        # -----------------------------------------------------

        my_referral_code = (
            existing_profile.get("referral_code")
            if existing_profile
            else None
        )

        if not my_referral_code:

            prefix = (
                "".join(
                    character
                    for character in clean_name.upper()
                    if character.isalnum()
                )[:3]
                or "USR"
            )

            suffix = "".join(
                random.choices(
                    string.ascii_uppercase
                    + string.digits,
                    k=6,
                )
            )

            my_referral_code = (
                f"NEAT-{prefix}{suffix}"
            )

        # -----------------------------------------------------
        # UPDATE AUTH USER
        # -----------------------------------------------------

        auth_payload = {
            "user_metadata": {
                "full_name": clean_name,
                "phone_number": f"+91{clean_phone}",
            }
        }

        if password:
            auth_payload["password"] = password

        if clean_email != (user.email or ""):
            auth_payload["email"] = clean_email

        try:
            CustomerRepository.update_auth_user(
                user_id=user_id,
                auth_payload=auth_payload,
            )

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        # -----------------------------------------------------
        # PROFILE
        # -----------------------------------------------------

        CustomerRepository.upsert_profile(
            user_id=user_id,
            full_name=clean_name,
            phone=clean_phone,
            address=(
                existing_profile.get("address")
                if existing_profile
                else ""
            ),
            pincode=(
                existing_profile.get("pincode")
                if existing_profile
                else ""
            ),
            email=clean_email,
            referral_code=my_referral_code,
            referred_by_id=referrer_id,
        )

        # -----------------------------------------------------
        # SIGNUP TABLE
        # -----------------------------------------------------

        CustomerRepository.upsert_signup(
            user_id=user_id,
            full_name=clean_name,
            email=clean_email,
            phone=clean_phone,
        )

        # -----------------------------------------------------
        # WALLET
        # -----------------------------------------------------

        CustomerRepository.upsert_wallet(
            user_id=user_id,
        )

        # -----------------------------------------------------
        # REFERRAL TRACKING + WELCOME COUPON
        # -----------------------------------------------------

        welcome_coupon_code = None

        if referrer_id:

            # -------------------------------------------------
            # CREATE REFERRAL
            # -------------------------------------------------

            CustomerRepository.create_referral(
                referrer_id=referrer_id,
                referred_user_id=user_id,
            )

            # -------------------------------------------------
            # GENERATE WELCOME COUPON
            # -------------------------------------------------

            welcome_coupon_code = (
                "WELCOME50_"
                + "".join(
                    random.choices(
                        string.ascii_uppercase
                        + string.digits,
                        k=4,
                    )
                )
            )

            # -------------------------------------------------
            # CREATE WELCOME COUPON
            # -------------------------------------------------

            CustomerRepository.create_welcome_coupon(
                coupon_code=welcome_coupon_code,
                phone=clean_phone,
            )

            # -------------------------------------------------
            # AUTH METADATA
            # -------------------------------------------------

            CustomerRepository.update_welcome_reward(
                user_id=user_id,
                coupon_code=welcome_coupon_code,
            )

        # -----------------------------------------------------
        # RETURN COMPLETE PROFILE
        # -----------------------------------------------------

        return (
            CustomerProfileService
            .get_profile(
                customer=customer,
            )
        )