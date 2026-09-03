from app.repositories.system_repository import SystemRepository


class SystemService:

    @staticmethod
    def test_connection():
        return SystemRepository.test_connection()