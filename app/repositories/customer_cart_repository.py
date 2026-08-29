from app.supabase.client import supabase


class CustomerCartRepository:
    # =========================================================
    # GET CART
    # =========================================================

    @staticmethod
    def get_cart(user_id: str):
        response = (
            supabase
            .table("cart_items")
            .select(
                """
                id,
                user_id,
                service_id,
                title,
                duration,
                price,
                image,
                created_at
                """
            )
            .eq("user_id", user_id)
            .order(
                "created_at",
                desc=True,
            )
            .execute()
        )

        return response.data or []

    # =========================================================
    # GET SINGLE CART ITEM
    # =========================================================

    @staticmethod
    def get_cart_item(
        user_id: str,
        service_id: str,
    ):
        response = (
            supabase
            .table("cart_items")
            .select(
                """
                id,
                user_id,
                service_id,
                title,
                duration,
                price,
                image,
                created_at
                """
            )
            .eq("user_id", user_id)
            .eq("service_id", service_id)
            .limit(1)
            .execute()
        )

        data = response.data or []

        return data[0] if data else None

    # =========================================================
    # GET SERVICE
    # =========================================================

    @staticmethod
    def get_service(service_id: str):
        response = (
            supabase
            .table("services")
            .select(
                """
                id,
                title,
                price,
                duration,
                image
                """
            )
            .eq("id", service_id)
            .limit(1)
            .execute()
        )

        data = response.data or []

        return data[0] if data else None

    # =========================================================
    # ADD CART ITEM
    # =========================================================

    @staticmethod
    def add_cart_item(
        user_id: str,
        service_id: str,
        title: str,
        duration: str | None,
        price: str,
        image: str | None,
    ):
        response = (
            supabase
            .table("cart_items")
            .insert(
                {
                    "user_id": user_id,
                    "service_id": service_id,
                    "title": title,
                    "duration": duration,
                    "price": price,
                    "image": image,
                }
            )
            .execute()
        )

        data = response.data or []

        return data[0] if data else None

    # =========================================================
    # REMOVE CART ITEM
    # =========================================================

    @staticmethod
    def remove_cart_item(
        user_id: str,
        service_id: str,
    ):
        response = (
            supabase
            .table("cart_items")
            .delete()
            .eq("user_id", user_id)
            .eq("service_id", service_id)
            .execute()
        )

        return response.data or []

    # =========================================================
    # CLEAR CART
    # =========================================================

    @staticmethod
    def clear_cart(user_id: str):
        response = (
            supabase
            .table("cart_items")
            .delete()
            .eq("user_id", user_id)
            .execute()
        )

        return response.data or []