from fastapi import HTTPException, status

from app.repositories.customer_wallet_repository import (
    CustomerWalletRepository,
)


class CustomerWalletService:

    # =========================================================
    # GET WALLET
    # =========================================================

    @staticmethod
    def get_wallet(user_id: str):

        wallet = (
            CustomerWalletRepository
            .get_wallet(user_id)
        )

        if not wallet:
            return {
                "success": True,
                "item": {
                    "user_id": user_id,
                    "balance": 0,
                    "updated_at": None,
                },
                "message": "Wallet fetched successfully.",
            }

        return {
            "success": True,
            "item": wallet,
            "message": "Wallet fetched successfully.",
        }

    # =========================================================
    # GET TRANSACTIONS
    # =========================================================

    @staticmethod
    def get_transactions(
        user_id: str,
        limit: int = 50,
    ):

        transactions = (
            CustomerWalletRepository
            .get_transactions(
                user_id=user_id,
                limit=limit,
            )
        )

        return {
            "success": True,
            "items": transactions,
            "message": (
                "Wallet transactions fetched successfully."
            ),
        }

    # =========================================================
    # DEDUCT WALLET
    # =========================================================

    @staticmethod
    def deduct_wallet(
        user_id: str,
        amount: float,
        description: str = "Booking payment",
    ):

        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wallet deduction amount must be greater than zero.",
            )

        wallet = (
            CustomerWalletRepository
            .get_wallet(user_id)
        )

        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wallet not found.",
            )

        balance = float(
            wallet.get("balance") or 0
        )

        if balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient wallet balance.",
            )

        CustomerWalletRepository.deduct_wallet(
            user_id=user_id,
            amount=amount,
        )

        CustomerWalletRepository.create_transaction(
            user_id=user_id,
            amount=-amount,
            transaction_type="booking_payment",
            description=description,
        )

        updated_wallet = (
            CustomerWalletRepository
            .get_wallet(user_id)
        )

        return {
            "success": True,
            "item": updated_wallet,
            "message": "Wallet amount deducted successfully.",
        }