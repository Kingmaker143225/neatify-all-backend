from app.supabase.client import supabase


class CustomerServiceRepository:

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _normalize_tax_percent(service: dict | None):
        """
        Normalize tax_percent values returned from Supabase.

        Examples:
            "4%"  -> 4.0
            "18%" -> 18.0
            "4"   -> 4.0
            4     -> 4.0
            None  -> None
        """

        if not service:
            return service

        value = service.get("tax_percent")

        if value is None:
            return service

        if isinstance(value, str):
            value = value.strip()

            # Remove percentage symbol
            if value.endswith("%"):
                value = value[:-1].strip()

            if not value:
                service["tax_percent"] = None
                return service

            try:
                service["tax_percent"] = float(value)
            except (ValueError, TypeError):
                service["tax_percent"] = None

        elif isinstance(value, (int, float)):
            service["tax_percent"] = float(value)

        else:
            service["tax_percent"] = None

        return service

    @staticmethod
    def _normalize_services(services: list):
        """
        Normalize tax_percent for all services.
        """

        normalized_services = []

        for service in services:
            normalized_service = (
                CustomerServiceRepository
                ._normalize_tax_percent(service)
            )

            normalized_services.append(
                normalized_service
            )

        return normalized_services

    # =========================================================
    # MAIN CATEGORIES
    # =========================================================

    @staticmethod
    def get_main_categories():

        response = (
            supabase
            .table("main_categories")
            .select(
                "id, name, icon_url, sort_order"
            )
            .order(
                "sort_order",
                desc=False,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # SERVICES
    # =========================================================

    @staticmethod
    def get_services(
        main_category_id: str | None = None,
        service_type: str | None = None,
    ):

        query = (
            supabase
            .table("services")
            .select("*")
        )

        if main_category_id:
            query = query.eq(
                "main_category_id",
                main_category_id,
            )

        if service_type:
            query = query.eq(
                "service_type",
                service_type,
            )

        response = (
            query
            .order(
                "sort_order",
                desc=False,
            )
            .execute()
        )

        services = response.data or []

        # -----------------------------------------------------
        # TEMPORARY DEBUG
        # -----------------------------------------------------

        # print(
        #     "🔥 RAW TAX:",
        #     [
        #         service.get("tax_percent")
        #         for service in services
        #     ],
        # )

        # normalized_services = (
        #     CustomerServiceRepository
        #     ._normalize_services(
        #         services
        #     )
        # )

        # print(
        #     "🔥 NORMALIZED TAX:",
        #     [
        #         service.get("tax_percent")
        #         for service in normalized_services
        #     ],
        # )

        # return normalized_services

        services = response.data or []

        return (
            CustomerServiceRepository
            ._normalize_services(
                services
            )
        )

    # =========================================================
    # SERVICE BY ID
    # =========================================================

    @staticmethod
    def get_service_by_id(
        service_id: str,
    ):

        response = (
            supabase
            .table("services")
            .select("*")
            .eq(
                "id",
                service_id,
            )
            .maybe_single()
            .execute()
        )

        service = response.data

        return (
            CustomerServiceRepository
            ._normalize_tax_percent(
                service
            )
        )

    # =========================================================
    # SERVICE BY SLUG
    # =========================================================

    @staticmethod
    def get_service_by_slug(
        slug: str,
    ):

        response = (
            supabase
            .table("services")
            .select("*")
            .eq(
                "slug",
                slug,
            )
            .maybe_single()
            .execute()
        )

        service = response.data

        return (
            CustomerServiceRepository
            ._normalize_tax_percent(
                service
            )
        )

    # =========================================================
    # ADD-ONS
    # =========================================================

    @staticmethod
    def get_active_addons(
        service_type: str | None = None,
    ):

        query = (
            supabase
            .table("add_ons")
            .select("*")
            .eq(
                "is_active",
                True,
            )
        )

        if service_type:
            query = query.ilike(
                "service_type",
                service_type.strip(),
            )

        response = (
            query
            .order(
                "sort_order",
                desc=False,
            )
            .execute()
        )

        return response.data or []