from datetime import time  # noqa: TC003
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo  # noqa: TC003

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseSettingsConfig(BaseSettings):
    """Base settings."""

    model_config = SettingsConfigDict(
        toml_file=["pyproject.toml", "settings.toml"],
        case_sensitive=False,
        validate_default=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customise sources for settings."""
        return (
            TomlConfigSettingsSource(settings_cls),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class SysSettings(BaseModel):
    """System application settings."""

    time_zone: ZoneInfo


class AlarmClockSettings(BaseModel):
    """Alarm clock settings."""

    start_time: time
    end_time: time
    delay: int = 30
    time_telling: bool


class ProjectSettings(BaseModel):
    """Pyproject information."""

    name: str = "unknown"
    version: str = "unknown"
    description: str = "unknown"


class LoggingSettings(BaseModel):
    """Logging settings."""

    log_level: LogLevel = "DEBUG"
    log_format: str = "%(asctime)s %(levelname)6s %(name)s: %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    directory: Path = Path("logs")
    log_file: str = "app.log"


class AppSettings(BaseSettingsConfig):
    """Application settings."""

    project: ProjectSettings
    settings: SysSettings
    alarm_settings: AlarmClockSettings
    logging: LoggingSettings = LoggingSettings()
