# from fastapi import APIRouter, Depends

# from app.dependencies.customer_auth import (
#     get_current_customer,
# )

# from app.schemas.customer_booking import (
#     CustomerBookingCreateRequest,
#     CustomerBookingResponse,
# )

# from app.services.customer_booking_service import (
#     CustomerBookingService,
# )


# router = APIRouter()


# # =========================================================
# # CREATE CUSTOMER BOOKING
# # =========================================================

# @router.post(
#     "/bookings",
#     response_model=CustomerBookingResponse,
# )
# async def create_customer_booking(
#     request: CustomerBookingCreateRequest,
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):

#     user_id = current_customer["user"].id

#     return (
#         CustomerBookingService
#         .create_booking(
#             user_id=str(user_id),
#             customer_name=request.customer_name,
#             email=request.email,
#             phone_number=request.phone_number,
#             full_address=request.full_address,
#             services=request.services,
#             booking_date=str(
#                 request.booking_date
#             ),
#             booking_time=request.booking_time,
#             total_amount=request.total_amount,
#         )
#     )


















# from fastapi import APIRouter, Depends

# from app.dependencies.customer_auth import (
#     get_current_customer,
# )

# from app.schemas.customer_booking import (
#     CustomerBookingCreateRequest,
#     CustomerBookingResponse,
# )

# from app.services.customer_booking_service import (
#     CustomerBookingService,
# )


# router = APIRouter()


# # =========================================================
# # CREATE CUSTOMER BOOKING
# # =========================================================

# @router.post(
#     "/bookings",
#     response_model=CustomerBookingResponse,
# )
# async def create_customer_booking(
#     request: CustomerBookingCreateRequest,
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):

#     user_id = current_customer["user"].id

#     return (
#         CustomerBookingService
#         .create_booking(
#             user_id=str(user_id),

#             customer_name=request.customer_name,

#             email=str(request.email),

#             phone_number=request.phone_number,

#             full_address=request.full_address,

#             services=request.services,

#             add_ons=request.add_ons,

#             booking_date=request.booking_date,

#             booking_time=request.booking_time,

#             latitude=request.latitude,

#             longitude=request.longitude,

#             location_link=request.location_link,
#         )
#     )
# # =========================================================
# # GET CUSTOMER BOOKINGS
# # =========================================================

# @router.get(
#     "/bookings",
# )
# async def get_customer_bookings(
#     current_customer=Depends(
#         get_current_customer
#     ),
# ):
#     user_id = current_customer["user"].id

#     bookings = (
#         CustomerBookingService
#         .get_customer_bookings(
#             user_id=str(user_id)
#         )
#     )

#     return {
#         "success": True,
#         "items": bookings,
#         "message": "Bookings fetched successfully.",
#     }




















from fastapi import APIRouter, Depends

from app.dependencies.customer_auth import (
    get_current_customer,
)

from app.schemas.customer_booking import (
    CustomerBookingCreateRequest,
    CustomerBookingResponse,
)

from app.services.customer_booking_service import (
    CustomerBookingService,
)


router = APIRouter()


# =========================================================
# CREATE CUSTOMER BOOKING
# =========================================================

@router.post(
    "/bookings",
    response_model=CustomerBookingResponse,
)
async def create_customer_booking(
    request: CustomerBookingCreateRequest,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = current_customer[
        "user"
    ].id

    return (
        CustomerBookingService
        .create_booking(
            user_id=str(user_id),

            customer_name=(
                request.customer_name
            ),

            email=str(
                request.email
            ),

            phone_number=(
                request.phone_number
            ),

            full_address=(
                request.full_address
            ),

            services=(
                request.services
            ),

            add_ons=(
                request.add_ons
            ),

            booking_date=(
                request.booking_date
            ),

            booking_time=(
                request.booking_time
            ),

            latitude=(
                request.latitude
            ),

            longitude=(
                request.longitude
            ),

            location_link=(
                request.location_link
            ),
        )
    )


# =========================================================
# GET CUSTOMER BOOKINGS
# =========================================================

@router.get(
    "/bookings",
)
async def get_customer_bookings(
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = current_customer[
        "user"
    ].id

    bookings = (
        CustomerBookingService
        .get_customer_bookings(
            user_id=str(user_id)
        )
    )

    return {
        "success": True,
        "items": bookings,
        "message": (
            "Bookings fetched successfully."
        ),
    }