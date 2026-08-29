# from fastapi import HTTPException, status

# from app.repositories.customer_repository import (
#     CustomerRepository,
# )
# from app.supabase.client import supabase


# class CustomerAuthService:

#     # =========================================================
#     # LOGIN
#     # =========================================================

#     @staticmethod
#     def login(
#         email: str,
#         password: str,
#     ):
#         try:
#             response = (
#                 supabase
#                 .auth
#                 .sign_in_with_password(
#                     {
#                         "email": email,
#                         "password": password,
#                     }
#                 )
#             )

#         except Exception as exc:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid email or password.",
#             ) from exc

#         if not response.session or not response.user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid email or password.",
#             )

#         user = response.user
#         session = response.session

#         user_id = str(user.id)
#         user_email = user.email or email

#         profile = (
#             CustomerRepository
#             .get_profile(user_id)
#         )

#         return {
#             "access_token": session.access_token,
#             "refresh_token": session.refresh_token,
#             "token_type": "bearer",
#             "user_id": user_id,
#             "email": user_email,
#             "profile_exists": profile is not None,
#         }

#     # =========================================================
#     # GET CURRENT USER
#     # =========================================================

#     @staticmethod
#     def get_current_user(
#         access_token: str,
#     ):
#         try:
#             response = (
#                 supabase
#                 .auth
#                 .get_user(access_token)
#             )

#         except Exception as exc:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired access token.",
#             ) from exc

#         if not response.user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired access token.",
#             )

#         return response.user

#     # =========================================================
#     # ME
#     # =========================================================

#     @staticmethod
#     def get_me(
#         access_token: str,
#     ):
#         user = (
#             CustomerAuthService
#             .get_current_user(
#                 access_token
#             )
#         )

#         user_id = str(user.id)

#         profile = (
#             CustomerRepository
#             .get_profile(user_id)
#         )

#         return {
#             "id": user_id,
#             "email": user.email or "",
#             "profile_exists": profile is not None,
#             "profile": profile,
#         }

#     # =========================================================
#     # LOGOUT
#     # =========================================================

#     @staticmethod
#     def logout(
#         access_token: str,
#     ):
#         # Validate the token before accepting logout.
#         CustomerAuthService.get_current_user(
#             access_token
#         )

#         # The mobile client will ultimately remove its
#         # local Supabase session. We intentionally do not
#         # call global supabase.auth.sign_out() here because
#         # the backend Supabase client is shared by requests.

#         return {
#             "success": True,
#             "message": "Customer logged out successfully.",
#         }

















import re

from fastapi import HTTPException, status

from app.repositories.customer_repository import (
    CustomerRepository,
)

from app.supabase.client import supabase


class CustomerAuthService:

    # =========================================================
    # PHONE NORMALIZATION
    # =========================================================

    @staticmethod
    def normalize_phone(phone: str) -> str:
        return "".join(
            character
            for character in phone
            if character.isdigit()
        )[-10:]

    # =========================================================
    # LOGIN
    # =========================================================

    @staticmethod
    def login(
        email: str,
        password: str,
    ):
        try:
            response = (
                supabase.auth.sign_in_with_password(
                    {
                        "email": email,
                        "password": password,
                    }
                )
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            ) from exc

        if not response.session or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        user = response.user
        session = response.session

        profile = (
            CustomerRepository
            .get_profile(str(user.id))
        )

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email or email,
            "profile_exists": profile is not None,
        }

    # =========================================================
    # SIGNUP
    # =========================================================

    @staticmethod
    def signup(
        full_name: str,
        email: str,
        phone: str,
        password: str,
    ):
        clean_name = full_name.strip()
        clean_phone = (
            CustomerAuthService
            .normalize_phone(phone)
        )

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

        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "full_name": clean_name,
                            "phone": clean_phone,
                        }
                    },
                }
            )

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        if not response.user:
            raise HTTPException(
                status_code=400,
                detail="Customer signup failed.",
            )

        user = response.user

        profile_created = False

        # -----------------------------------------------------
        # Create customer profile when Supabase returns
        # a user immediately.
        # -----------------------------------------------------

        try:
            CustomerRepository.upsert_profile(
                user_id=str(user.id),
                full_name=clean_name,
                phone=clean_phone,
                address="",
                pincode="",
                email=email,
            )

            profile_created = True

        except Exception:
            # Auth user was created successfully.
            # Profile can be completed later.
            profile_created = False

        email_confirmation_required = (
            getattr(user, "email_confirmed_at", None)
            is None
        )

        return {
            "user_id": str(user.id),
            "email": user.email or email,
            "profile_created": profile_created,
            "email_confirmation_required": (
                email_confirmation_required
            ),
            "message": (
                "Signup successful. "
                "Please confirm your email."
                if email_confirmation_required
                else "Signup successful."
            ),
        }

    # =========================================================
    # CURRENT USER
    # =========================================================

    @staticmethod
    def get_current_user(
        access_token: str,
    ):
        try:
            response = (
                supabase.auth.get_user(
                    access_token
                )
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token.",
            ) from exc

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token.",
            )

        return response.user

    # =========================================================
    # PROFILE COMPLETENESS
    # =========================================================

    @staticmethod
    def get_profile_completeness(
        access_token: str,
    ):
        user = (
            CustomerAuthService
            .get_current_user(
                access_token
            )
        )

        user_id = str(user.id)

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        email_confirmed = (
            getattr(
                user,
                "email_confirmed_at",
                None,
            )
            is not None
        )

        missing_fields = []

        if not profile:
            missing_fields.extend(
                [
                    "full_name",
                    "email",
                    "phone",
                ]
            )
        else:
            if not profile.get("full_name"):
                missing_fields.append(
                    "full_name"
                )

            if not (
                profile.get("email")
                or user.email
            ):
                missing_fields.append(
                    "email"
                )

            if not profile.get("phone"):
                missing_fields.append(
                    "phone"
                )

        if not email_confirmed:
            missing_fields.append(
                "email_confirmation"
            )

        return {
            "profile_exists": profile is not None,
            "profile_complete": (
                len(missing_fields) == 0
            ),
            "email_confirmed": email_confirmed,
            "missing_fields": missing_fields,
        }

    # =========================================================
    # ME
    # =========================================================

    @staticmethod
    def get_me(
        access_token: str,
    ):
        user = (
            CustomerAuthService
            .get_current_user(
                access_token
            )
        )

        user_id = str(user.id)

        profile = (
            CustomerRepository
            .get_profile(user_id)
        )

        completeness = (
            CustomerAuthService
            .get_profile_completeness(
                access_token
            )
        )

        return {
            "id": user_id,
            "email": user.email or "",
            "email_confirmed": (
                getattr(
                    user,
                    "email_confirmed_at",
                    None,
                )
                is not None
            ),
            "profile_exists": profile is not None,
            "profile_complete": (
                completeness[
                    "profile_complete"
                ]
            ),
            "profile": profile,
        }

    # =========================================================
    # SEND OTP
    # =========================================================

    @staticmethod
    def send_otp(
        phone: str,
    ):
        clean_phone = (
            CustomerAuthService
            .normalize_phone(phone)
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=400,
                detail="Phone number must be exactly 10 digits.",
            )

        try:
            response = (
                supabase.functions.invoke(
                    "msg91-send-otp",
                    {
                        "body": {
                            "phone": clean_phone,
                        }
                    },
                )
            )

        # except Exception as exc:
        #     raise HTTPException(
        #         status_code=502,
        #         detail="Failed to send OTP.",
        #     ) from exc
        except Exception as exc:
            print("❌ MSG91 SEND OTP ERROR:", repr(exc))

            raise HTTPException(
                status_code=502,
                detail=str(exc),
            ) from exc

        data = response.get("data")

        if isinstance(data, dict) and data.get("error"):
            raise HTTPException(
                status_code=400,
                detail=data["error"],
            )

        return {
            "success": True,
            "message": "OTP sent successfully.",
        }

    # =========================================================
    # VERIFY OTP
    # =========================================================

    @staticmethod
    def verify_otp(
        phone: str,
        otp: str,
    ):
        clean_phone = (
            CustomerAuthService
            .normalize_phone(phone)
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=400,
                detail="Phone number must be exactly 10 digits.",
            )

        if not otp:
            raise HTTPException(
                status_code=400,
                detail="OTP is required.",
            )

        try:
            response = (
                supabase.functions.invoke(
                    "msg91-verify-otp",
                    {
                        "body": {
                            "phone": clean_phone,
                            "otp": otp,
                        }
                    },
                )
            )

        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to verify OTP.",
            ) from exc

        data = response.get("data")

        if not isinstance(data, dict):
            raise HTTPException(
                status_code=502,
                detail="Invalid OTP service response.",
            )

        if data.get("error"):
            raise HTTPException(
                status_code=400,
                detail=data["error"],
            )

        is_new_user = bool(
            data.get("isNewUser")
        )

        if is_new_user:
            return {
                "success": True,
                "is_new_user": True,
                "email": None,
                "temp_password": None,
                "message": (
                    "OTP verified. "
                    "Customer profile can be completed."
                ),
            }

        return {
            "success": True,
            "is_new_user": False,
            "email": data.get("email"),
            "temp_password": data.get(
                "tempPassword"
            ),
            "message": (
                "OTP verified successfully."
            ),
        }
        # =========================================================
    # CUSTOMER REWARDS / OFFERS
    # =========================================================

    @staticmethod
    def get_rewards(
        access_token: str,
    ):
        user = (
            CustomerAuthService
            .get_current_user(
                access_token
            )
        )

        metadata = getattr(
            user,
            "user_metadata",
            None,
        ) or {}

        return {
            "show_welcome_reward": bool(
                metadata.get(
                    "show_welcome_reward",
                    False,
                )
            ),
            "welcome_coupon_code": metadata.get(
                "welcome_coupon_code"
            ),
            "show_signup_offer_popup": bool(
                metadata.get(
                    "show_signup_offer_popup",
                    False,
                )
            ),
            "signup_service_title": metadata.get(
                "signup_service_title"
            ),
            "signup_service_id": metadata.get(
                "signup_service_id"
            ),
        }

    @staticmethod
    def update_rewards(
        access_token: str,
        show_welcome_reward: bool | None = None,
        show_signup_offer_popup: bool | None = None,
    ):
        user = (
            CustomerAuthService
            .get_current_user(
                access_token
            )
        )

        metadata = getattr(
            user,
            "user_metadata",
            None,
        ) or {}

        update_data = {}

        if show_welcome_reward is not None:
            update_data[
                "show_welcome_reward"
            ] = show_welcome_reward

        if show_signup_offer_popup is not None:
            update_data[
                "show_signup_offer_popup"
            ] = show_signup_offer_popup

        if update_data:
            metadata.update(update_data)

            try:
                response = (
                    supabase.auth.admin.update_user_by_id(
                        str(user.id),
                        {
                            "user_metadata": metadata
                        },
                    )
                )
            except Exception as exc:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to update customer rewards.",
                ) from exc

            updated_user = getattr(
                response,
                "user",
                None,
            )

            if updated_user:
                metadata = (
                    getattr(
                        updated_user,
                        "user_metadata",
                        None,
                    )
                    or metadata
                )

        return {
            "show_welcome_reward": bool(
                metadata.get(
                    "show_welcome_reward",
                    False,
                )
            ),
            "welcome_coupon_code": metadata.get(
                "welcome_coupon_code"
            ),
            "show_signup_offer_popup": bool(
                metadata.get(
                    "show_signup_offer_popup",
                    False,
                )
            ),
            "signup_service_title": metadata.get(
                "signup_service_title"
            ),
            "signup_service_id": metadata.get(
                "signup_service_id"
            ),
        }

    # =========================================================
    # LOGOUT
    # =========================================================

    @staticmethod
    def logout(
        access_token: str,
    ):
        CustomerAuthService.get_current_user(
            access_token
        )

        return {
            "success": True,
            "message": "Customer logged out successfully.",
        }