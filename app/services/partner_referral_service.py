from app.repositories.partner_referral_repository import (
    PartnerReferralRepository,
)


class PartnerReferralService:

    @staticmethod
    def get_referral_summary(
        partner_id: str,
    ):
        # =====================================================
        # PARTNER PROFILE
        # =====================================================

        profile = (
            PartnerReferralRepository
            .get_partner_profile(partner_id)
        )

        referral_code = (
            profile.get("referral_code")
            if profile
            else None
        )

        # =====================================================
        # REFERRED PARTNERS
        # =====================================================

        referred_partners = (
            PartnerReferralRepository
            .get_referred_partners(partner_id)
        )

        referral_count = len(
            referred_partners
        )

        # =====================================================
        # REFERRAL FORMS
        # =====================================================

        referral_form_ids = [
            item.get("referral_form_id")
            for item in referred_partners
            if item.get("referral_form_id")
        ]

        referral_forms = (
            PartnerReferralRepository
            .get_referral_forms(
                referral_form_ids
            )
        )

        forms_by_id = {
            str(item["id"]): item
            for item in referral_forms
        }

        # =====================================================
        # TOTAL PAID REWARDS
        # =====================================================

        total_rewards = 0

        for form in referral_forms:
            if form.get("bonus_status") == "paid":
                total_rewards += float(
                    form.get("bonus_amount") or 0
                )

        # =====================================================
        # RESPONSE
        # =====================================================

        return {
            "referral_code":
                referral_code or "",

            "referral_count":
                referral_count,

            "total_rewards":
                total_rewards,
        }

    @staticmethod
    def get_referral_history(
        partner_id: str,
    ):
        # =====================================================
        # REFERRED PARTNERS
        # =====================================================

        referred_partners = (
            PartnerReferralRepository
            .get_referred_partners(partner_id)
        )

        if not referred_partners:
            return {
                "total_rewards": 0,
                "referrals": [],
            }

        # =====================================================
        # REFERRAL FORMS
        # =====================================================

        referral_form_ids = [
            item.get("referral_form_id")
            for item in referred_partners
            if item.get("referral_form_id")
        ]

        referral_forms = (
            PartnerReferralRepository
            .get_referral_forms(
                referral_form_ids
            )
        )

        forms_by_id = {
            str(item["id"]): item
            for item in referral_forms
        }

        # =====================================================
        # BUILD HISTORY
        # =====================================================

        referrals = []
        total_rewards = 0

        for partner in referred_partners:

            form_id = partner.get(
                "referral_form_id"
            )

            form = forms_by_id.get(
                str(form_id)
            )

            completed_booking = int(
                form.get(
                    "completed_booking"
                ) or 0
            ) if form else 0

            bonus_status = (
                form.get("bonus_status")
                if form
                else "pending"
            )

            bonus_amount = float(
                form.get("bonus_amount") or 0
            ) if form else 0

            if bonus_status == "paid":
                total_rewards += bonus_amount

            referrals.append(
                {
                    "id": str(
                        partner.get("id")
                    ),

                    "name":
                        partner.get(
                            "name"
                        )
                        or "Partner",

                    "completed_booking":
                        completed_booking,

                    "bonus_status":
                        bonus_status,

                    "bonus_amount":
                        bonus_amount,
                }
            )

        return {
            "total_rewards":
                total_rewards,

            "referrals":
                referrals,
        }