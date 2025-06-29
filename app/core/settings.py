from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    admin_secret_key: str = "553b0b2b-7b93-4f07-8b1d-b75896883503"
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def __init__(self, **data):
        super().__init__(**data)


settings = Settings()
