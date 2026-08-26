from app.supabase.client import supabase


class PartnerReferralRepository:

    @staticmethod
    def get_partner_profile(partner_id: str):
        response = (
            supabase
            .table("staff_profile")
            .select("referral_code")
            .eq("id", partner_id)
            .single()
            .execute()
        )

        return response.data

    @staticmethod
    def get_referred_partners(partner_id: str):
        response = (
            supabase
            .table("staff_profile")
            .select(
                "id, name, referral_form_id"
            )
            .eq("referred_by", partner_id)
            .execute()
        )

        return response.data or []

    @staticmethod
    def get_referral_forms(
        referral_form_ids: list[str],
    ):
        if not referral_form_ids:
            return []

        response = (
            supabase
            .table("staff_referral_forms")
            .select(
                "id, completed_booking, bonus_status, bonus_amount"
            )
            .in_("id", referral_form_ids)
            .execute()
        )

        return response.data or []