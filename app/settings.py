import os


class Settings:
    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self.app_name = os.getenv("APP_NAME", "ml_scoring_service")


settings = Settings()
