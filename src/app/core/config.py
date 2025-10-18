from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo


_settings = Dynaconf(
    settings_files=["config.yml"]
)

_project_timezone = "Europe/Moscow"


_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.postgres.user,
    password=_settings.postgres.password,
    host=_settings.postgres.host,
    port=_settings.postgres.port,
    path=_settings.postgres.db,
)


class Settings1(BaseSettings):
    app_name: str
    timezone: str
    tz: ZoneInfo
    app_env: str

    db_dsn: str
    redis_dsn: str
    kafka_dsn: str

settings = Settings1(
    app_name="fastapi-example",
    timezone=_project_timezone,
    tz=ZoneInfo(_project_timezone),
    app_env=_settings.app_env,
    db_dsn=str(_db_dsn),
    redis_dsn=str(_settings.redis.url),
    kafka_dsn=str(_settings.kafka.url),
)   