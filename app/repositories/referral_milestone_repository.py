from app.supabase.admin_client import supabase_admin


class ReferralMilestoneRepository:

    # =========================================================
    # 30-BOOKING REFERRAL MILESTONES
    # =========================================================

    @staticmethod
    def get_pending_30_booking_milestones():
        response = (
            supabase_admin
            .table("staff_referral_forms")
            .select("*")
            .gte("completed_booking", 30)
            .eq("bonus_notification_sent", False)
            .eq("status", "approved")
            .execute()
        )

        return response.data or []

    # =========================================================
    # REFERRAL REWARD PAID
    # =========================================================

    @staticmethod
    def get_pending_paid_rewards():
        response = (
            supabase_admin
            .table("staff_referral_forms")
            .select("*")
            .eq("bonus_status", "paid")
            .eq("reward_paid_notification_sent", False)
            .eq("status", "approved")
            .execute()
        )

        return response.data or []

    # =========================================================
    # FIND REFERRER
    # =========================================================

    @staticmethod
    def get_referrer_by_code(referral_code: str):
        response = (
            supabase_admin
            .table("staff_profile")
            .select("id, email, push_token")
            .eq("referral_code", referral_code)
            .maybe_single()
            .execute()
        )

        return response.data

    # =========================================================
    # STORE NOTIFICATION
    # =========================================================

    @staticmethod
    def create_notification(data: dict):
        response = (
            supabase_admin
            .table("notifications")
            .insert(data)
            .execute()
        )

        return response.data or []

    # =========================================================
    # MARK 30-BOOKING NOTIFICATION SENT
    # =========================================================

    @staticmethod
    def mark_bonus_notification_sent(referral_id: str):
        response = (
            supabase_admin
            .table("staff_referral_forms")
            .update({
                "bonus_notification_sent": True,
            })
            .eq("id", referral_id)
            .execute()
        )

        return response.data or []

    # =========================================================
    # MARK REWARD-PAID NOTIFICATION SENT
    # =========================================================

    @staticmethod
    def mark_reward_paid_notification_sent(
        referral_id: str,
    ):
        response = (
            supabase_admin
            .table("staff_referral_forms")
            .update({
                "reward_paid_notification_sent": True,
            })
            .eq("id", referral_id)
            .execute()
        )

        return response.data or []