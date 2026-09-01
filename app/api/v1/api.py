# from fastapi import APIRouter

# from app.api.v1.endpoints.system import router as system_router
# from app.api.v1.endpoints.auth import router as auth_router
# from app.api.v1.endpoints.partner import router as partner_router

# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )

# api_router = APIRouter()


# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )













# from fastapi import APIRouter

# from app.api.v1.endpoints.system import router as system_router
# from app.api.v1.endpoints.auth import router as auth_router
# from app.api.v1.endpoints.partner import router as partner_router
# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )

# from app.api.v1.endpoints.admin import (
#     router as admin_router,
# )


# api_router = APIRouter()


# # =========================================================
# # SYSTEM
# # =========================================================

# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# # =========================================================
# # AUTHENTICATION
# # =========================================================

# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )


# # =========================================================
# # PARTNER
# # =========================================================

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )


# # =========================================================
# # PARTNER DUTY
# # =========================================================

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )


# # =========================================================
# # ADMIN
# # =========================================================

# api_router.include_router(
#     admin_router,
#     prefix="/admin",
#     tags=["Admin"],
# )




















# from fastapi import APIRouter

# from app.api.v1.endpoints.system import router as system_router
# from app.api.v1.endpoints.auth import router as auth_router
# from app.api.v1.endpoints.partner import router as partner_router
# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )


# api_router = APIRouter()


# # =========================================================
# # SYSTEM
# # =========================================================

# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# # =========================================================
# # AUTHENTICATION
# # =========================================================

# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )


# # =========================================================
# # PARTNER
# # =========================================================

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )


# # =========================================================
# # PARTNER DUTY
# # =========================================================

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )















# from fastapi import APIRouter

# from app.api.v1.endpoints.system import (
#     router as system_router,
# )

# from app.api.v1.endpoints.auth import (
#     router as auth_router,
# )

# from app.api.v1.endpoints.partner import (
#     router as partner_router,
# )

# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )

# from app.api.v1.endpoints.admin import (
#     router as admin_router,
# )


# api_router = APIRouter()


# # =========================================================
# # SYSTEM
# # =========================================================

# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# # =========================================================
# # AUTHENTICATION
# # =========================================================

# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )


# # =========================================================
# # PARTNER
# # =========================================================

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )


# # =========================================================
# # PARTNER DUTY
# # =========================================================

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )


# # =========================================================
# # ADMIN
# # =========================================================

# api_router.include_router(
#     admin_router,
#     prefix="/admin",
#     tags=["Admin"],
# )






















# from fastapi import APIRouter

# from app.api.v1.endpoints.system import (
#     router as system_router,
# )

# from app.api.v1.endpoints.auth import (
#     router as auth_router,
# )

# from app.api.v1.endpoints.partner import (
#     router as partner_router,
# )

# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )

# from app.api.v1.endpoints.admin import (
#     router as admin_router,
# )

# from app.api.v1.endpoints.booking_reminder import router as booking_reminder_router



# from app.api.v1.endpoints.notification import (
#     router as notification_router,
# )

# from app.api.v1.endpoints.referral_milestone import (
#     router as referral_milestone_router,
# )


# from app.api.v1.endpoints.partner_payment import (
#     router as partner_payment_router,
# )


# from app.api.v1.endpoints.referral_bonus import (
#     router as referral_bonus_router,
# )

# from app.api.v1.endpoints.referral_reward import (
#     router as referral_reward_router,
# )

# from app.api.v1.endpoints.staff_notification import (
#     router as staff_notification_router,
# )
# api_router = APIRouter()


# # =========================================================
# # SYSTEM
# # =========================================================

# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# # =========================================================
# # AUTHENTICATION
# # =========================================================

# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )


# # =========================================================
# # PARTNER
# # =========================================================

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )


# # =========================================================
# # PARTNER DUTY
# # =========================================================

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )


# # =========================================================
# # ADMIN
# # =========================================================

# api_router.include_router(
#     admin_router,
#     prefix="/admin",
#     tags=["Admin"],
# )

# api_router.include_router(
#     booking_reminder_router,
#     prefix="/system",
#     tags=["Booking Reminders"],
# )

# api_router.include_router(
#     notification_router,
#     prefix="/notifications",
#     tags=["Notifications"],
# )


# api_router.include_router(
#     referral_milestone_router,
#     prefix="/system",
#     tags=["Referral Milestones"],
# )

# api_router.include_router(
#     partner_payment_router,
#     prefix="/partner",
#     tags=["Partner Payment"],
# )

# api_router.include_router(
#     referral_bonus_router,
#     prefix="/partner",
#     tags=["Referral Bonus"],
# )


# api_router.include_router(
#     referral_reward_router,
#     prefix="/partner",
#     tags=["Referral Reward"],
# )

# api_router.include_router(
#     staff_notification_router,
#     prefix="/notifications",
#     tags=["Staff Notification"],
# )



















# from fastapi import APIRouter

# from app.api.v1.endpoints.system import (
#     router as system_router,
# )

# from app.api.v1.endpoints.auth import (
#     router as auth_router,
# )

# from app.api.v1.endpoints.partner import (
#     router as partner_router,
# )

# from app.api.v1.endpoints.partner_duty import (
#     router as partner_duty_router,
# )

# from app.api.v1.endpoints.admin import (
#     router as admin_router,
# )

# from app.api.v1.endpoints.booking_reminder import router as booking_reminder_router



# from app.api.v1.endpoints.notification import (
#     router as notification_router,
# )

# from app.api.v1.endpoints.referral_milestone import (
#     router as referral_milestone_router,
# )


# from app.api.v1.endpoints.partner_payment import (
#     router as partner_payment_router,
# )


# from app.api.v1.endpoints.referral_bonus import (
#     router as referral_bonus_router,
# )

# from app.api.v1.endpoints.referral_reward import (
#     router as referral_reward_router,
# )

# # from app.api.v1.endpoints.staff_notification import (
# #     router as staff_notification_router,
# # )
# api_router = APIRouter()


# # =========================================================
# # SYSTEM
# # =========================================================

# api_router.include_router(
#     system_router,
#     prefix="/system",
#     tags=["System"],
# )


# # =========================================================
# # AUTHENTICATION
# # =========================================================

# api_router.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"],
# )


# # =========================================================
# # PARTNER
# # =========================================================

# api_router.include_router(
#     partner_router,
#     prefix="/partner",
#     tags=["Partner"],
# )


# # =========================================================
# # PARTNER DUTY
# # =========================================================

# api_router.include_router(
#     partner_duty_router,
#     prefix="/partner",
#     tags=["Partner Duty"],
# )


# # =========================================================
# # ADMIN
# # =========================================================

# api_router.include_router(
#     admin_router,
#     prefix="/admin",
#     tags=["Admin"],
# )

# api_router.include_router(
#     booking_reminder_router,
#     prefix="/system",
#     tags=["Booking Reminders"],
# )

# api_router.include_router(
#     notification_router,
#     prefix="/notifications",
#     tags=["Notifications"],
# )


# api_router.include_router(
#     referral_milestone_router,
#     prefix="/system",
#     tags=["Referral Milestones"],
# )

# api_router.include_router(
#     partner_payment_router,
#     prefix="/partner",
#     tags=["Partner Payment"],
# )

# api_router.include_router(
#     referral_bonus_router,
#     prefix="/partner",
#     tags=["Referral Bonus"],
# )


# api_router.include_router(
#     referral_reward_router,
#     prefix="/partner",
#     tags=["Referral Reward"],
# )

# # api_router.include_router(
# #     staff_notification_router,
# #     prefix="/notifications",
# #     tags=["Staff Notification"],
# # )



















from fastapi import APIRouter

from app.api.v1.endpoints.system import (
    router as system_router,
)

from app.api.v1.endpoints.auth import (
    router as auth_router,
)

from app.api.v1.endpoints.partner import (
    router as partner_router,
)

from app.api.v1.endpoints.partner_duty import (
    router as partner_duty_router,
)

from app.api.v1.endpoints.admin import (
    router as admin_router,
)

from app.api.v1.endpoints.booking_reminder import router as booking_reminder_router



from app.api.v1.endpoints.notification import (
    router as notification_router,
)

from app.api.v1.endpoints.referral_milestone import (
    router as referral_milestone_router,
)


from app.api.v1.endpoints.partner_payment import (
    router as partner_payment_router,
)


from app.api.v1.endpoints.referral_bonus import (
    router as referral_bonus_router,
)

from app.api.v1.endpoints.referral_reward import (
    router as referral_reward_router,
)

from app.api.v1.endpoints.customer_auth import (
    router as customer_auth_router,
)


from app.api.v1.endpoints.customer_profile import (
    router as customer_profile_router,
)


from app.api.v1.endpoints.customer_services import (
    router as customer_services_router,
)

from app.api.v1.endpoints.customer_booking import (
    router as customer_booking_router,
)

from app.api.v1.endpoints.customer_payment import (
    router as customer_payment_router,
)

from app.api.v1.endpoints.customer_cart import (
    router as customer_cart_router,
)

from app.api.v1.endpoints import customer_home

from app.api.v1.endpoints import customer_coupon
# from app.api.v1.endpoints.staff_notification import (
#     router as staff_notification_router,
# )

from app.api.v1.endpoints import customer_policy
api_router = APIRouter()

from app.api.v1.endpoints import customer_wallet

from app.api.v1.endpoints import customer_referral

from fastapi import APIRouter
from app.api.v1.endpoints.customer_auth import router as customer_auth_router


# =========================================================
# SYSTEM
# =========================================================

api_router.include_router(
    system_router,
    prefix="/system",
    tags=["System"],
)


# =========================================================
# AUTHENTICATION
# =========================================================

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


# =========================================================
# PARTNER
# =========================================================

api_router.include_router(
    partner_router,
    prefix="/partner",
    tags=["Partner"],
)


# =========================================================
# PARTNER DUTY
# =========================================================

api_router.include_router(
    partner_duty_router,
    prefix="/partner",
    tags=["Partner Duty"],
)


# =========================================================
# ADMIN
# =========================================================

api_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"],
)

api_router.include_router(
    booking_reminder_router,
    prefix="/system",
    tags=["Booking Reminders"],
)

api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["Notifications"],
)


api_router.include_router(
    referral_milestone_router,
    prefix="/system",
    tags=["Referral Milestones"],
)

api_router.include_router(
    partner_payment_router,
    prefix="/partner",
    tags=["Partner Payment"],
)

api_router.include_router(
    referral_bonus_router,
    prefix="/partner",
    tags=["Referral Bonus"],
)


api_router.include_router(
    referral_reward_router,
    prefix="/partner",
    tags=["Referral Reward"],
)

# =========================================================
# CUSTOMER AUTHENTICATION
# =========================================================

api_router.include_router(
    customer_auth_router,
    prefix="/customer/auth",
    tags=["Customer Authentication"],
)

api_router.include_router(
    customer_profile_router,
    prefix="/customer/profile",
    tags=["Customer Profile"],
)


api_router.include_router(
    customer_services_router,
    prefix="/customer",
    tags=["Customer Services"],
)

api_router.include_router(
    customer_booking_router,
    prefix="/customer",
    tags=["Customer Booking"],
)

api_router.include_router(
    customer_payment_router,
    prefix="/customer",
    tags=["Customer Payment"],
)

api_router.include_router(
    customer_cart_router,
    prefix="/customer/cart",
    tags=["Customer Cart"],
)

api_router.include_router(
    customer_home.router,
    prefix="/customer",
    tags=["Customer Home"],
)

api_router.include_router(
    customer_coupon.router,
    prefix="/customer",
    tags=["Customer Coupon"],
)

api_router.include_router(
    customer_policy.router,
    prefix="/customer",
    tags=["Customer Policy"],
)


api_router.include_router(
    customer_wallet.router,
    prefix="/customer",
    tags=["Customer Wallet"],
)

api_router.include_router(
    customer_referral.router,
    prefix="/customer",
    tags=["Customer Referral"],
)

api_router.include_router(
    customer_auth_router,
    prefix="/customer/auth",
    tags=["Customer Authentication"],
)
