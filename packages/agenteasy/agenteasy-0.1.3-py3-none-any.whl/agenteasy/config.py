from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # Redis相关
    REDIS_ENDPOINT: str = "xxxx:xxx"
    REDIS_PASSWORD: str = "xxxx"
    REDIS_URL_PREFIX: str = "rediss"

    # Mongo相关
    MONGO_URL: str = "mongodb+srv://xxxx/"

    MONGO_DB_NAME: str = "xxx"
    MONGO_COLLECTION_NAME: str = "test"

    # 测试模式
    DEBUG: bool = False

    @property
    def REDIS_URL(self):
        return f"{self.REDIS_URL_PREFIX}://default:{self.REDIS_PASSWORD}@{self.REDIS_ENDPOINT}"


settings = Settings()
