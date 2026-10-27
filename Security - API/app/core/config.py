from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_drivername: str = "postgresql+asyncpg"
    db_username: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_database: str

    secret_key: str
    jwt_algorithm: str
    jwt_token_expiration_time: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
