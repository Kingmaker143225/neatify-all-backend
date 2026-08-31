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

#     user_id = current_customer[
#         "user"
#     ].id

#     return (
#         CustomerBookingService
#         .create_booking(
#             user_id=str(user_id),

#             customer_name=(
#                 request.customer_name
#             ),

#             email=str(
#                 request.email
#             ),

#             phone_number=(
#                 request.phone_number
#             ),

#             full_address=(
#                 request.full_address
#             ),

#             services=(
#                 request.services
#             ),

#             add_ons=(
#                 request.add_ons
#             ),

#             booking_date=(
#                 request.booking_date
#             ),

#             booking_time=(
#                 request.booking_time
#             ),

#             latitude=(
#                 request.latitude
#             ),

#             longitude=(
#                 request.longitude
#             ),

#             location_link=(
#                 request.location_link
#             ),
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

#     user_id = current_customer[
#         "user"
#     ].id

#     bookings = (
#         CustomerBookingService
#         .get_customer_bookings(
#             user_id=str(user_id)
#         )
#     )

#     return {
#         "success": True,
#         "items": bookings,
#         "message": (
#             "Bookings fetched successfully."
#         ),
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


# =========================================================
# GET SINGLE CUSTOMER BOOKING
# =========================================================

@router.get(
    "/bookings/{booking_id}",
    response_model=CustomerBookingResponse,
)
async def get_customer_booking(
    booking_id: str,
    current_customer=Depends(
        get_current_customer
    ),
):

    user_id = current_customer[
        "user"
    ].id

    booking = (
        CustomerBookingService
        .get_booking(
            booking_id=booking_id,
            user_id=str(user_id),
        )
    )

    return booking


# =========================================================
# CHECK CUSTOMER SERVICE AVAILABILITY
# =========================================================

@router.get(
    "/service-availability",
)
async def check_customer_service_availability(
    pincode: str,
    service_categories: str,
    current_customer=Depends(
        get_current_customer
    ),
):
    categories = [
        category.strip()
        for category in service_categories.split(",")
        if category.strip()
    ]

    if not categories:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="At least one service category is required.",
        )

    result = (
        CustomerBookingService
        .check_service_availability(
            pincode=pincode,
            service_categories=categories,
        )
    )

    return result