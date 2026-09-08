import re
import jwt
import hashlib
import secrets
import httpx

# from urllib.parse import urlencode



from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.repositories.customer_repository import (
    CustomerRepository,
)

from app.supabase.client import supabase
from app.supabase.admin_client import supabase_admin
from app.config.settings import settings


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

        # return {
        #     "id": user_id,
        #     "email": user.email or "",
        #     "email_confirmed": (
        #         getattr(
        #             user,
        #             "email_confirmed_at",
        #             None,
        #         )
        #         is not None
        #     ),
        #     "profile_exists": profile is not None,
        #     "profile_complete": (
        #         completeness[
        #             "profile_complete"
        #         ]
        #     ),
        #     "profile": profile,
        # }


        profile_email = (
            profile.get("email")
            if profile and profile.get("email")
            else user.email or ""
        )

        return {
            "id": user_id,
            "email": profile_email,
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

        # -----------------------------------------------------
        # FORMAT PHONE
        # -----------------------------------------------------

        formatted_phone = f"91{clean_phone}"

        # -----------------------------------------------------
        # CHECK MSG91 CONFIGURATION
        # -----------------------------------------------------

        if not settings.msg91_auth_key:
            raise HTTPException(
                status_code=500,
                detail="MSG91 authentication key is not configured.",
            )

        # -----------------------------------------------------
        # GENERATE 6 DIGIT OTP
        # -----------------------------------------------------

        otp_code = str(
            secrets.randbelow(900000) + 100000
        )

        # -----------------------------------------------------
        # HASH OTP
        # -----------------------------------------------------

        otp_hash = hashlib.sha256(
            otp_code.encode("utf-8")
        ).hexdigest()

        # -----------------------------------------------------
        # OTP EXPIRY - 5 MINUTES
        # -----------------------------------------------------

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=5)
        ).isoformat()

        # -----------------------------------------------------
        # SAVE OTP TO DATABASE
        # -----------------------------------------------------

        try:
            db_response = (
                supabase_admin
                .table("phone_otp_verifications")
                .upsert(
                    {
                        "phone": formatted_phone,
                        "otp_hash": otp_hash,
                        "expires_at": expires_at,
                        "attempts": 0,
                        "verified_at": None,
                    },
                    on_conflict="phone",
                )
                .execute()
            )

        except Exception as exc:
            print(
                "❌ OTP DATABASE ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to save OTP.",
            ) from exc

        # -----------------------------------------------------
        # MSG91 WHATSAPP PAYLOAD
        # -----------------------------------------------------

        payload = {
            "integrated_number": (
                settings.msg91_integrated_number
            ),
            "content_type": "template",
            "payload": {
                "messaging_product": "whatsapp",
                "type": "template",
                "template": {
                    "name": (
                        settings.msg91_otp_template_name
                    ),
                    "language": {
                        "code": "en",
                        "policy": "deterministic",
                    },
                    "namespace": (
                        settings.msg91_otp_namespace
                    ),
                    "to_and_components": [
                        {
                            "to": [
                                formatted_phone
                            ],
                            "components": {
                                "body_1": {
                                    "type": "text",
                                    "value": str(
                                        otp_code
                                    ),
                                },
                                "button_1": {
                                    "subtype": "url",
                                    "type": "text",
                                    "value": str(
                                        otp_code
                                    ),
                                },
                            },
                        }
                    ],
                },
            },
        }

        # -----------------------------------------------------
        # SEND OTP THROUGH MSG91
        # -----------------------------------------------------

        try:
            with httpx.Client(
                timeout=20
            ) as client:

                response = client.post(
                    settings.msg91_url,
                    headers={
                        "authkey": (
                            settings.msg91_auth_key
                        ),
                        "Content-Type": (
                            "application/json"
                        ),
                    },
                    json=payload,
                )

            try:
                response_data = response.json()
            except Exception:
                response_data = {
                    "raw_response": response.text
                }

            print(
                "📲 MSG91 OTP HTTP Status:",
                response.status_code,
            )

            print(
                "📲 MSG91 OTP Response:",
                response_data,
            )

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": (
                            "MSG91 WhatsApp OTP API failed."
                        ),
                        "status_code": (
                            response.status_code
                        ),
                        "response": response_data,
                    },
                )

        except httpx.RequestError as exc:
            print(
                "❌ MSG91 CONNECTION ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "Unable to connect to MSG91 WhatsApp API."
                ),
            ) from exc

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

        formatted_phone = f"91{clean_phone}"

        # -----------------------------------------------------
        # FETCH OTP RECORD
        # -----------------------------------------------------

        try:
            response = (
                supabase_admin
                .table("phone_otp_verifications")
                .select("*")
                .eq(
                    "phone",
                    formatted_phone,
                )
                .maybe_single()
                .execute()
            )

            record = response.data

        except Exception as exc:
            print(
                "❌ OTP DATABASE FETCH ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to fetch OTP record.",
            ) from exc

        # -----------------------------------------------------
        # OTP RECORD NOT FOUND
        # -----------------------------------------------------

        if not record:
            raise HTTPException(
                status_code=400,
                detail=(
                    "OTP Record not found. "
                    "Please request a new OTP."
                ),
            )

        # -----------------------------------------------------
        # ALREADY VERIFIED
        # -----------------------------------------------------

        if record.get("verified_at"):
            raise HTTPException(
                status_code=400,
                detail="This OTP has already been verified.",
            )

        # -----------------------------------------------------
        # MAX ATTEMPTS
        # -----------------------------------------------------

        attempts = int(
            record.get("attempts") or 0
        )

        if attempts >= 3:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many failed attempts. "
                    "Please request a new OTP."
                ),
            )

        # -----------------------------------------------------
        # EXPIRY CHECK
        # -----------------------------------------------------

        expires_at = record.get(
            "expires_at"
        )

        if not expires_at:
            raise HTTPException(
                status_code=400,
                detail=(
                    "OTP has expired. "
                    "Please request a new one."
                ),
            )

        try:
            expiry_datetime = (
                datetime.fromisoformat(
                    str(expires_at).replace(
                        "Z",
                        "+00:00",
                    )
                )
            )

            if expiry_datetime < datetime.now(
                timezone.utc
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "OTP has expired. "
                        "Please request a new one."
                    ),
                )

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=(
                    "OTP has expired. "
                    "Please request a new one."
                )
            )

        # -----------------------------------------------------
        # HASH INPUT OTP
        # -----------------------------------------------------

        input_hash = hashlib.sha256(
            str(otp).encode("utf-8")
        ).hexdigest()

        stored_hash = str(
            record.get("otp_hash") or ""
        )

        # -----------------------------------------------------
        # OTP MISMATCH
        # -----------------------------------------------------

        if input_hash != stored_hash:

            new_attempts = attempts + 1

            try:
                (
                    supabase_admin
                    .table(
                        "phone_otp_verifications"
                    )
                    .update(
                        {
                            "attempts": new_attempts
                        }
                    )
                    .eq(
                        "phone",
                        formatted_phone,
                    )
                    .execute()
                )

            except Exception as exc:
                print(
                    "❌ OTP ATTEMPT UPDATE ERROR:",
                    repr(exc),
                )

            remaining_attempts = (
                2 - attempts
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid OTP. You have "
                    f"{remaining_attempts} "
                    f"attempts remaining."
                ),
            )

        # -----------------------------------------------------
        # MARK OTP VERIFIED
        # -----------------------------------------------------

        try:
            (
                supabase_admin
                .table(
                    "phone_otp_verifications"
                )
                .update(
                    {
                        "verified_at": (
                            datetime.now(
                                timezone.utc
                            ).isoformat()
                        )
                    }
                )
                .eq(
                    "phone",
                    formatted_phone,
                )
                .execute()
            )

        except Exception as exc:
            print(
                "❌ OTP VERIFY UPDATE ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to verify OTP.",
            ) from exc

        # =====================================================
        # SUPABASE AUTH USER
        # =====================================================

        formatted_phone_with_plus = (
            f"+{formatted_phone}"
        )

        dummy_email = (
            f"{formatted_phone}@phone.neatify.app"
        )

        # -----------------------------------------------------
        # FIND EXISTING CUSTOMER
        # -----------------------------------------------------

        user = None
        is_new_user = False

        try:
            # -------------------------------------------------
            # FIRST: FIND CUSTOMER PROFILE BY PHONE
            # -------------------------------------------------

            profile_response = (
                supabase_admin
                .table("profile")
                .select("id, phone, email, full_name")
                .in_(
                    "phone",
                    [
                        clean_phone,
                        f"91{clean_phone}",
                        f"+91{clean_phone}",
                    ],
                )
                .limit(1)
                .execute()
            )

            profiles = profile_response.data or []
            profile = profiles[0] if profiles else None

            print(
                "🔎 Profile lookup result:",
                profile,
            )

            if profile and profile.get("id"):

                profile_user_id = str(profile["id"])

                print(
                    "✅ Existing customer profile found:",
                    profile_user_id,
                )

                # -------------------------------------------------
                # GET EXISTING SUPABASE AUTH USER BY PROFILE ID
                # -------------------------------------------------

                user_response = (
                    supabase_admin
                    .auth.admin
                    .get_user_by_id(
                        profile_user_id
                    )
                )

                user = getattr(
                    user_response,
                    "user",
                    None,
                )

                if user:
                    print(
                        "✅ Existing Supabase Auth user found:",
                        user.id,
                    )

        except Exception as exc:
            print(
                "⚠️ EXISTING CUSTOMER LOOKUP ERROR:",
                repr(exc),
            )

        # -----------------------------------------------------
        # FIND EXISTING AUTH USER BY EMAIL
        # -----------------------------------------------------

        if not user:
            try:
                print(
                    "🔎 Looking for existing Auth user by email:",
                    dummy_email,
                )

                users_response = (
                    supabase_admin
                    .auth.admin
                    .list_users(
                        page=1,
                        per_page=1000,
                    )
                )

                print("🔎 list_users response type:", type(users_response))
                print("🔎 list_users response:", repr(users_response))

                # Supabase SDK versions return the users differently.
                users = getattr(users_response, "users", None)

                if users is None:
                    users = getattr(users_response, "data", None)

                if users is None and isinstance(users_response, list):
                    users = users_response

                users = users or []

                print("🔎 Total Auth users received:", len(users))

                for existing_user in users:
                    existing_email = getattr(existing_user, "email", None)

                    if existing_email and existing_email.lower() == dummy_email.lower():
                        user = existing_user

                        print(
                            "✅ Existing Supabase Auth user found:",
                            user.id,
                            existing_email,
                        )
                        break

            except Exception as exc:
                print("❌ Auth user lookup error:", repr(exc))
                user = None

        # -----------------------------------------------------
        # CREATE USER ONLY IF AUTH USER DOES NOT EXIST
        # -----------------------------------------------------

        if not user:
            try:
                print(
                    "🆕 No existing Auth user found. Creating new customer:",
                    dummy_email,
                )

                new_user_response = (
                    supabase_admin
                    .auth.admin
                    .create_user(
                        {
                            "email": dummy_email,
                            "email_confirm": True,
                            "phone": formatted_phone,
                            "phone_confirm": True,
                            "user_metadata": {
                                "phone": clean_phone,
                            },
                        }
                    )
                )

                user = getattr(
                    new_user_response,
                    "user",
                    None,
                )

                if not user:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to create customer account.",
                    )

                is_new_user = True

                print(
                    "✅ New Supabase Auth user created:",
                    user.id,
                )

            except Exception as exc:
                print(
                    "❌ SUPABASE USER CREATE ERROR:",
                    repr(exc),
                )

                raise HTTPException(
                    status_code=500,
                    detail="Failed to create customer account.",
                ) from exc

        # -----------------------------------------------------
        # EXISTING USER / NEW USER STATUS
        # -----------------------------------------------------

        if user:
            user_metadata = (
                getattr(
                    user,
                    "user_metadata",
                    None,
                )
                or {}
            )

            if not user_metadata.get("full_name"):
                is_new_user = True

        # =====================================================
        # GENERATE AUTH SESSION
        # =====================================================

        user_email = getattr(user, "email", None) or dummy_email

        try:
            link_response = (
                supabase_admin
                .auth.admin
                .generate_link(
                    {
                        "type": "magiclink",
                        "email": user_email,
                    }
                )
            )

            properties = getattr(
                link_response,
                "properties",
                None,
            )

            email_otp = (
                getattr(
                    properties,
                    "email_otp",
                    None,
                )
                if properties
                else None
            )

            if not email_otp:
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "Failed to generate authentication token."
                    ),
                )

            auth_response = (
                supabase
                .auth
                .verify_otp(
                    {
                        "email": user_email,
                        "token": email_otp,
                        "type": "magiclink",
                    }
                )
            )

        except HTTPException:
            raise

        except Exception as exc:
            print(
                "❌ SUPABASE SESSION ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to create authentication session."
                ),
            ) from exc

        session = getattr(
            auth_response,
            "session",
            None,
        )

        if not session:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Authentication session could not be created."
                ),
            )

        # =====================================================
        # RETURN
        # =====================================================

        return {
            "success": True,
            "is_new_user": is_new_user,
            "email": (
                # user.email
                # if user
                # else dummy_email

                profile.get("email")
                if profile and profile.get("email")
                else ""
            ),
            "temp_password": None,
            "access_token": (
                session.access_token
            ),
            "refresh_token": (
                session.refresh_token
            ),
            "token_type": "bearer",
            "user_id": (
                str(user.id)
                if user
                else None
            ),
            "message": (
                "OTP verified. "
                "Customer profile can be completed."
                if is_new_user
                else "OTP verified successfully."
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
    # MSG91 WIDGET AUTHENTICATION
    # =========================================================

    @staticmethod
    def verify_msg91_widget_token(
        access_token: str,
    ):
        """
        Verify MSG91 Widget access token and create/login
        the corresponding Neatify customer.
        """

        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="MSG91 access token is required.",
            )

        # -----------------------------------------------------
        # VERIFY ACCESS TOKEN WITH MSG91
        # -----------------------------------------------------

        try:
            # with httpx.Client(timeout=20) as client:
            #     response = client.post(
            #         settings.msg91_verify_access_token_url,
            #         headers={
            #             "Content-Type": "application/json",
            #         },
            #         data={
            #             "authkey": settings.msg91_auth_key,
            #             "access-token": access_token,
            #         },
            #     )
        
            print(
                "📤 MSG91 AUTH KEY PRESENT:",
                bool(settings.msg91_auth_key),
            )

            print(
                "📤 MSG91 ACCESS TOKEN PRESENT:",
                bool(access_token),
            )

            print(
                "📤 MSG91 VERIFY URL:",
                settings.msg91_verify_access_token_url,
            )

            with httpx.Client(timeout=20) as client:
                response = client.post(
                    settings.msg91_verify_access_token_url,
                    headers={
                        "Content-Type": "application/json",
                        "authkey": settings.msg91_auth_key,
                    },
                    json={
                        "access-token": access_token,
                    },
                )

                # print("📤 REQUEST METHOD:", http_request.method)
                # print("📤 REQUEST URL:", http_request.url)
                # print(
                #     "📤 REQUEST CONTENT-TYPE:",
                #     http_request.headers.get("content-type"),
                # )
                # print(
                #     "📤 REQUEST BODY LENGTH:",
                #     len(http_request.content),
                # )

                # response = client.send(http_request)
            try:
                response_data = response.json()
            except Exception:
                response_data = {
                    "raw_response": response.text,
                }

            print(
                "📲 MSG91 VERIFY ACCESS TOKEN STATUS:",
                response.status_code,
            )

            print(
                "📲 MSG91 VERIFY ACCESS TOKEN RESPONSE:",
                response_data,
            )

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=401,
                    detail={
                        "message": "MSG91 access token verification failed.",
                        "response": response_data,
                    },
                )

        except HTTPException:
            raise

        except httpx.RequestError as exc:
            print(
                "❌ MSG91 VERIFY ACCESS TOKEN CONNECTION ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=502,
                detail="Unable to connect to MSG91.",
            ) from exc

        # -----------------------------------------------------
        # EXTRACT VERIFIED MOBILE
        # -----------------------------------------------------

        msg91_data = response_data.get("data") or {}

        verified_phone = (
            response_data.get("message")
            or msg91_data.get("mobile")
            or msg91_data.get("phone")
            or msg91_data.get("identifier")
        )

        if not verified_phone:
            print(
                "❌ MSG91 verification response did not contain mobile:",
                response_data,
            )
            raise HTTPException(
                status_code=401,
                detail="MSG91 did not return a verified mobile number.",
            )

        verified_phone = str(verified_phone).replace("+", "").strip()

        print("✅ MSG91 VERIFIED MOBILE:", verified_phone)

        if not verified_phone:
            print(
                "❌ MSG91 verification response did not contain mobile:",
                response_data,
            )

            raise HTTPException(
                status_code=401,
                detail="MSG91 did not return a verified mobile number.",
            )

        clean_phone = (
            CustomerAuthService.normalize_phone(
                str(verified_phone)
            )
        )

        if len(clean_phone) != 10:
            raise HTTPException(
                status_code=400,
                detail="Invalid verified mobile number.",
            )

        formatted_phone = f"91{clean_phone}"

        dummy_email = (
            f"{formatted_phone}@phone.neatify.app"
        )

        # -----------------------------------------------------
        # FIND EXISTING CUSTOMER PROFILE
        # -----------------------------------------------------

        user = None
        profile = None
        is_new_user = False

        try:
            profile_response = (
                supabase_admin
                .table("profile")
                .select(
                    "id, phone, email, full_name"
                )
                .in_(
                    "phone",
                    [
                        clean_phone,
                        formatted_phone,
                        f"+{formatted_phone}",
                    ],
                )
                .limit(1)
                .execute()
            )

            profiles = profile_response.data or []
            profile = (
                profiles[0]
                if profiles
                else None
            )

            print(
                "🔎 MSG91 customer profile lookup:",
                profile,
            )

            if profile and profile.get("id"):
                user_response = (
                    supabase_admin
                    .auth.admin
                    .get_user_by_id(
                        str(profile["id"])
                    )
                )

                user = getattr(
                    user_response,
                    "user",
                    None,
                )

        except Exception as exc:
            print(
                "❌ MSG91 CUSTOMER LOOKUP ERROR:",
                repr(exc),
            )

        # -----------------------------------------------------
        # FALLBACK: FIND PHONE LOGIN AUTH USER
        # -----------------------------------------------------

        if not user:
            try:
                users_response = (
                    supabase_admin
                    .auth.admin
                    .list_users(
                        page=1,
                        per_page=1000,
                    )
                )

                users = getattr(
                    users_response,
                    "users",
                    None,
                )

                if users is None:
                    users = getattr(
                        users_response,
                        "data",
                        None,
                    )

                if users is None and isinstance(
                    users_response,
                    list,
                ):
                    users = users_response

                users = users or []

                for existing_user in users:
                    existing_email = getattr(
                        existing_user,
                        "email",
                        None,
                    )

                    if (
                        existing_email
                        and existing_email.lower()
                        == dummy_email.lower()
                    ):
                        user = existing_user
                        break

            except Exception as exc:
                print(
                    "❌ MSG91 AUTH USER LOOKUP ERROR:",
                    repr(exc),
                )

        # -----------------------------------------------------
        # CREATE CUSTOMER AUTH USER
        # -----------------------------------------------------

        if not user:
            try:
                new_user_response = (
                    supabase_admin
                    .auth.admin
                    .create_user(
                        {
                            "email": dummy_email,
                            "email_confirm": True,
                            "phone": formatted_phone,
                            "phone_confirm": True,
                            "user_metadata": {
                                "phone": clean_phone,
                            },
                        }
                    )
                )

                user = getattr(
                    new_user_response,
                    "user",
                    None,
                )

                if not user:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to create customer account.",
                    )

                is_new_user = True

                print(
                    "✅ MSG91 new customer created:",
                    user.id,
                )

            except HTTPException:
                raise

            except Exception as exc:
                print(
                    "❌ MSG91 CUSTOMER CREATE ERROR:",
                    repr(exc),
                )

                raise HTTPException(
                    status_code=500,
                    detail="Failed to create customer account.",
                ) from exc

        # -----------------------------------------------------
        # DETERMINE NEW USER / PROFILE COMPLETION
        # -----------------------------------------------------

        user_metadata = (
            getattr(
                user,
                "user_metadata",
                None,
            )
            or {}
        )

        if not user_metadata.get("full_name"):
            is_new_user = True

        # -----------------------------------------------------
        # CREATE CUSTOMER PROFILE FOR NEW USER
        # -----------------------------------------------------

        if not profile:
            try:
                CustomerRepository.upsert_profile(
                    user_id=str(user.id),
                    full_name="",
                    phone=clean_phone,
                    address="",
                    pincode="",
                    email=(
                        ""
                        if dummy_email
                        else ""
                    ),
                )

                print(
                    "✅ MSG91 customer profile created:",
                    user.id,
                )

                profile = (
                    CustomerRepository
                    .get_profile(
                        str(user.id)
                    )
                )

            except Exception as exc:
                print(
                    "❌ MSG91 PROFILE CREATE ERROR:",
                    repr(exc),
                )

                raise HTTPException(
                    status_code=500,
                    detail="Failed to create customer profile.",
                ) from exc

        # -----------------------------------------------------
        # GENERATE SUPABASE SESSION
        # -----------------------------------------------------

        user_email = (
            getattr(user, "email", None)
            or dummy_email
        )

        try:
            link_response = (
                supabase_admin
                .auth.admin
                .generate_link(
                    {
                        "type": "magiclink",
                        "email": user_email,
                    }
                )
            )

            properties = getattr(
                link_response,
                "properties",
                None,
            )

            email_otp = (
                getattr(
                    properties,
                    "email_otp",
                    None,
                )
                if properties
                else None
            )

            if not email_otp:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate authentication token.",
                )

            auth_response = (
                supabase
                .auth
                .verify_otp(
                    {
                        "email": user_email,
                        "token": email_otp,
                        "type": "magiclink",
                    }
                )
            )

        except HTTPException:
            raise

        except Exception as exc:
            print(
                "❌ MSG91 SUPABASE SESSION ERROR:",
                repr(exc),
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to create authentication session.",
            ) from exc

        session = getattr(
            auth_response,
            "session",
            None,
        )

        if not session:
            raise HTTPException(
                status_code=500,
                detail="Authentication session could not be created.",
            )

        # -----------------------------------------------------
        # RETURN STANDARD CUSTOMER AUTH RESPONSE
        # -----------------------------------------------------

        return {
            "success": True,
            "is_new_user": is_new_user,
            "email": (
                profile.get("email")
                if profile
                and profile.get("email")
                else ""
            ),
            "message": (
                "MSG91 OTP verified. "
                "Customer profile can be completed."
                if is_new_user
                else "MSG91 OTP verified successfully."
            ),
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user_id": str(user.id),
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

    # =========================================================
    # ✅ GOOGLE OAUTH HELPERS (NEW)
    # =========================================================

    @staticmethod
    def _create_backend_token(user_id: str) -> str:
        """
        Create a JWT token for the user.
        This token will be used by the frontend for subsequent API calls.
        """
        try:
            payload = {
                "sub": user_id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "iat": datetime.utcnow(),
            }
            
            token = jwt.encode(
                payload,
                settings.secret_key,
                algorithm="HS256"
            )
            
            return token
            
        except Exception as e:
            print(f"❌ [GoogleAuth] Failed to create token: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create authentication token: {str(e)}"
            )

    @staticmethod
    def _get_profile_completeness_for_user(user_id: str) -> dict:
        """
        Get profile completeness for a user by ID.
        Used internally for Google OAuth flow.
        """
        profile = CustomerRepository.get_profile(user_id)
        
        if not profile:
            return {
                "profile_exists": False,
                "profile_complete": False,
                "missing_fields": ["full_name", "email", "phone"]
            }
        
        missing_fields = []
        if not profile.get("full_name"):
            missing_fields.append("full_name")
        if not profile.get("email"):
            missing_fields.append("email")
        if not profile.get("phone"):
            missing_fields.append("phone")
        
        return {
            "profile_exists": True,
            "profile_complete": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }

    # =========================================================
    # CUSTOMER REWARDS / OFFERS
    # =========================================================

    @staticmethod
    def get_rewards(
        access_token: str,
    ):
        user = CustomerAuthService.get_current_user(
            access_token
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
        user = CustomerAuthService.get_current_user(
            access_token
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
                    or {}
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