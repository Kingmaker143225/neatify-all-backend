from fastapi import HTTPException, status

from app.repositories.customer_service_repository import (
    CustomerServiceRepository,
)


class CustomerServiceService:

    # =========================================================
    # MAIN CATEGORIES
    # =========================================================

    @staticmethod
    def get_main_categories():

        return (
            CustomerServiceRepository
            .get_main_categories()
        )

    # =========================================================
    # SERVICES
    # =========================================================

    @staticmethod
    def get_services(
        main_category_id: str | None = None,
        service_type: str | None = None,
    ):

        return (
            CustomerServiceRepository
            .get_services(
                main_category_id=main_category_id,
                service_type=service_type,
            )
        )

    # =========================================================
    # SERVICE BY ID
    # =========================================================

    @staticmethod
    def get_service_by_id(
        service_id: str,
    ):

        service = (
            CustomerServiceRepository
            .get_service_by_id(
                service_id=service_id,
            )
        )

        if not service:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found.",
            )

        return service

    # =========================================================
    # SERVICE BY SLUG
    # =========================================================

    @staticmethod
    def get_service_by_slug(
        slug: str,
    ):

        service = (
            CustomerServiceRepository
            .get_service_by_slug(
                slug=slug,
            )
        )

        if not service:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found.",
            )

        return service

    # =========================================================
    # ADD-ONS
    # =========================================================

    @staticmethod
    def get_active_addons(
        service_type: str | None = None,
    ):

        return (
            CustomerServiceRepository
            .get_active_addons(
                service_type=service_type,
            )
        )