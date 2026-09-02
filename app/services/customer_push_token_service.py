from app.repositories.customer_push_token_repository import (
    CustomerPushTokenRepository,
)


class CustomerPushTokenService:

    # =========================================================
    # SAVE PUSH TOKEN
    # =========================================================

    @staticmethod
    def save_token(
        user_id: str,
        token: str,
        platform: str,
    ):

        # Remove this token from any previous account.
        CustomerPushTokenRepository.delete_by_token(
            token=token,
        )

        # Attach it to the current customer.
        CustomerPushTokenRepository.upsert_token(
            user_id=user_id,
            token=token,
            platform=platform,
        )

        return {
            "success": True,
            "message": "Push token saved successfully.",
        }

    # =========================================================
    # REMOVE PUSH TOKEN
    # =========================================================

    @staticmethod
    def remove_token(
        user_id: str,
        token: str,
    ):

        CustomerPushTokenRepository.delete_token(
            user_id=user_id,
            token=token,
        )

        return {
            "success": True,
            "message": "Push token removed successfully.",
        }