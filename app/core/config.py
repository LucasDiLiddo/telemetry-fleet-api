from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Telemetry Fleet API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Seguridad / JWT
    SECRET_KEY: str = "super_secret_key_para_desarrollo_cambiar_en_prod_123456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    # Base de Datos (SQLite por defecto para desarrollo local sin Docker)
    DATABASE_URL: str = "sqlite:///./fleet_database.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()