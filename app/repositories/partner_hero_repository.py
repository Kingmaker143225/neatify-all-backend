from app.supabase.client import supabase


class PartnerHeroRepository:

    @staticmethod
    def get_hero_images():
        response = (
            supabase
            .table("hero_images")
            .select("*")
            .eq("is_active", True)
            .order("priority", desc=False)
            .execute()
        )

        images = response.data or []

        for image in images:
            image_path = image.get("image_path")

            if image_path:
                public_url = (
                    supabase
                    .storage
                    .from_("hero-images-staff")
                    .get_public_url(image_path)
                )

                image["image_url"] = public_url

        return images