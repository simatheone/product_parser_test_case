from functools import lru_cache

from pydantic import BaseSettings, RedisDsn


class AppSettings(BaseSettings):
    """Application settings."""

    ALLOW_ORIGINS: list[str]
    DB_ENGINE: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def database_url(self) -> str:
        """Url for connection to database.

        Returns:
        - str: The URL used to connect to the database based on the settings
        stored in the `AppSettings` instance.

        Raises:
        - None.
        """

        return (
            f'{self.DB_ENGINE}://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


@lru_cache
def get_settings():
    """Retrieves the application's settings and returns an instance of the
    `AppSettings` class containing these settings.

    Returns:
    - AppSettings: An instance of `AppSettings` with the application's settings.

    Raises:
    - None.
    """

    return AppSettings()  # type: ignore


settings = get_settings()
