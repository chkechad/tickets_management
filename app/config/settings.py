"""settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):  # type: ignore[misc]
    """base config."""

    ENV_STATE: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    """global config."""

    DATABASE_URL: str | None = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    """dev config."""

    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    """prod config."""

    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    """test config."""

    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache
def get_config(env_state: str) -> GlobalConfig:
    """Instantiate config based on the environment."""
    configs: dict[str, type[GlobalConfig]] = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config: GlobalConfig = get_config(env_state=GlobalConfig().ENV_STATE)
