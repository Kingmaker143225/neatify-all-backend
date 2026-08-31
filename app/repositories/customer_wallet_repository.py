from app.supabase.client import supabase


class CustomerWalletRepository:

    # =========================================================
    # GET WALLET
    # =========================================================

    @staticmethod
    def get_wallet(user_id: str):

        response = (
            supabase
            .table("wallet")
            .select(
                """
                user_id,
                balance,
                updated_at
                """
            )
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # GET WALLET TRANSACTIONS
    # =========================================================

    @staticmethod
    def get_transactions(
        user_id: str,
        limit: int = 50,
    ):

        response = (
            supabase
            .table("wallet_transactions")
            .select(
                """
                id,
                user_id,
                amount,
                transaction_type,
                description,
                created_at
                """
            )
            .eq("user_id", user_id)
            .order(
                "created_at",
                desc=True,
            )
            .limit(limit)
            .execute()
        )

        return response.data or []

    # =========================================================
    # DEDUCT WALLET
    # =========================================================

    @staticmethod
    def deduct_wallet(
        user_id: str,
        amount: float,
    ):

        wallet = (
            CustomerWalletRepository
            .get_wallet(user_id)
        )

        if not wallet:
            return None

        current_balance = float(
            wallet.get("balance") or 0
        )

        if current_balance < amount:
            return None

        new_balance = (
            current_balance - amount
        )

        response = (
            supabase
            .table("wallet")
            .update(
                {
                    "balance": new_balance,
                }
            )
            .eq("user_id", user_id)
            .execute()
        )

        return response.data

    # =========================================================
    # CREATE TRANSACTION
    # =========================================================

    @staticmethod
    def create_transaction(
        user_id: str,
        amount: float,
        transaction_type: str,
        description: str,
    ):

        response = (
            supabase
            .table("wallet_transactions")
            .insert(
                {
                    "user_id": user_id,
                    "amount": amount,
                    "transaction_type": transaction_type,
                    "description": description,
                }
            )
            .execute()
        )

        return response.data