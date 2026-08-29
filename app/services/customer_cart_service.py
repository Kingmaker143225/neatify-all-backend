from fastapi import HTTPException, status

from app.repositories.customer_cart_repository import (
    CustomerCartRepository,
)


class CustomerCartService:

    # =========================================================
    # GET CART
    # =========================================================

    @staticmethod
    def get_cart(
        user_id: str,
    ):
        items = CustomerCartRepository.get_cart(
            user_id=user_id,
        )

        return {
            "success": True,
            "items": items,
            "message": "Cart fetched successfully.",
        }

    # =========================================================
    # ADD ITEM
    # =========================================================

    @staticmethod
    def add_to_cart(
        user_id: str,
        service_id: str,
    ):
        service_id = service_id.strip()

        if not service_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service ID is required.",
            )

        # -----------------------------------------------------
        # CHECK SERVICE
        # -----------------------------------------------------

        service = CustomerCartRepository.get_service(
            service_id=service_id,
        )

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found.",
            )

        # -----------------------------------------------------
        # CHECK DUPLICATE
        # -----------------------------------------------------

        existing_item = (
            CustomerCartRepository.get_cart_item(
                user_id=user_id,
                service_id=service_id,
            )
        )

        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already in Cart",
            )

        # -----------------------------------------------------
        # GET SERVICE DATA
        # -----------------------------------------------------

        title = service.get("title")

        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid service.",
            )

        price = service.get("price")

        if price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service price is unavailable.",
            )

        duration = service.get("duration")
        image = service.get("image")

        # -----------------------------------------------------
        # INSERT
        # -----------------------------------------------------

        item = CustomerCartRepository.add_cart_item(
            user_id=user_id,
            service_id=service_id,
            title=str(title),
            duration=(
                str(duration)
                if duration is not None
                else None
            ),
            price=str(price),
            image=(
                str(image)
                if image is not None
                else None
            ),
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add service to cart.",
            )

        return {
            "success": True,
            "item": item,
            "message": "Service added to cart.",
        }

    # =========================================================
    # REMOVE ITEM
    # =========================================================

    @staticmethod
    def remove_from_cart(
        user_id: str,
        service_id: str,
    ):
        service_id = service_id.strip()

        if not service_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service ID is required.",
            )

        existing_item = (
            CustomerCartRepository.get_cart_item(
                user_id=user_id,
                service_id=service_id,
            )
        )

        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found.",
            )

        CustomerCartRepository.remove_cart_item(
            user_id=user_id,
            service_id=service_id,
        )

        return {
            "success": True,
            "message": "Service removed from cart.",
        }

    # =========================================================
    # CLEAR CART
    # =========================================================

    @staticmethod
    def clear_cart(
        user_id: str,
    ):
        CustomerCartRepository.clear_cart(
            user_id=user_id,
        )

        return {
            "success": True,
            "message": "Cart cleared successfully.",
        }
    