from app.repositories.partner_hero_repository import (
    PartnerHeroRepository,
)


class PartnerHeroService:

    @staticmethod
    def get_hero_images():
        return PartnerHeroRepository.get_hero_images()