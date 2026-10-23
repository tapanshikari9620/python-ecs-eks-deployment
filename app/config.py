import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    environment: str
    log_level: str
    api_message: str


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "python-demo-app"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        api_message=os.getenv(
            "API_MESSAGE",
            "Hello from the Python Demo API!",
        ),
    )
