from app.supabase.client import supabase


class CustomerHomeService:

    # =========================================================
    # HERO BANNERS
    # =========================================================

    @staticmethod
    def get_hero_banners():

        response = (
            supabase
            .from_("hero_banners")
            .select("image_path")
            .eq("is_active", True)
            .order("priority")
            .execute()
        )

        return response.data or []


    # =========================================================
    # POPUPS
    # =========================================================

    @staticmethod
    def get_popups():

        response = (
            supabase
            .from_("app_popups")
            .select("*")
            .eq("is_active", True)
            .execute()
        )

        return response.data or []


    # =========================================================
    # OFFERS
    # =========================================================

    @staticmethod
    def get_offers():

        response = (
            supabase
            .from_("offers")
            .select("*")
            .eq("is_offer_enabled", True)
            .execute()
        )

        return response.data or []


    # =========================================================
    # WHY CHOOSE US
    # =========================================================

    @staticmethod
    def get_why_choose_us():

        return {
            "title": "Why Choose Neatify?",
            "subtitle": "We make home services simple, reliable and stress-free.",
            "features": [
                {
                    "icon": "shield-check-outline",
                    "iconFamily": "MaterialCommunityIcons",
                    "title": "Verified & Trained Professionals",
                    "description": "Skilled experts you can trust.",
                },
                {
                    "icon": "pricetag-outline",
                    "iconFamily": "Ionicons",
                    "title": "Transparent Pricing",
                    "description": "No hidden charges. Pay what you see.",
                },
                {
                    "icon": "time-outline",
                    "iconFamily": "Ionicons",
                    "title": "On-Time Service",
                    "description": "Punctual and reliable service at your doorstep.",
                },
                {
                    "icon": "happy-outline",
                    "iconFamily": "Ionicons",
                    "title": "Customer Satisfaction",
                    "description": "We ensure quality service every time.",
                },
            ],
            "bottom_title": "Ready to make your home feel new?",
            "bottom_desc": "Book a service now and experience the Neatify difference.",
            "bottom_button_text": "Book a Service Now",
        }