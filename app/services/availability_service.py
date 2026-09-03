# from fastapi import HTTPException

# from app.repositories.availability_repository import (
#     AvailabilityRepository,
# )


# class AvailabilityService:

#     @staticmethod
#     def get_availability(
#         email: str,
#         month: str,
#     ):
#         result = (
#             AvailabilityRepository.get_availability(
#                 email=email,
#                 month=month,
#             )
#         )

#         if not result:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Staff profile not found.",
#             )

#         return {
#             "success": True,
#             "data": result,
#         }

#     @staticmethod
#     def save_availability(
#         email: str,
#         month: str,
#         calendar_data: dict,
#     ):
#         result = (
#             AvailabilityRepository.save_availability(
#                 email=email,
#                 month=month,
#                 calendar_data=calendar_data,
#             )
#         )

#         if result is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Staff profile not found.",
#             )

#         return {
#             "success": True,
#             "message": "Availability updated successfully.",
#             "data": result,
#         }













from fastapi import HTTPException

from app.repositories.availability_repository import (
    AvailabilityRepository,
)


class AvailabilityService:

    @staticmethod
    def get_availability(
        email: str,
        month: str,
    ):
        result = AvailabilityRepository.get_availability(
            email=email,
            month=month,
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found.",
            )

        return {
            "success": True,
            "data": result,
        }

    @staticmethod
    def save_availability(
        email: str,
        month: str,
        calendar_data: dict,
    ):
        result = AvailabilityRepository.save_availability(
            email=email,
            month=month,
            calendar_data=calendar_data,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found.",
            )

        return {
            "success": True,
            "message": "Availability updated successfully.",
            "data": result,
        }