from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: str
    URL: str


@dataclass
class TgBot:
    token: str
    use_redis: bool
    admin_ids: list[int]
    manager_ids: list[int]
    worker_ids: list[int]


@dataclass
class Redis:
    host: str
    password: str
    port: str


@dataclass
class Config:
    bot: TgBot
    redis: Redis
    db: DbConfig


def get_conf(path: str = ".env"):
    env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            manager_ids=list(map(int, env.list("MANAGERS"))),
            worker_ids=list(map(int, env.list("WORKERS"))),
        ),
        redis=Redis(
            host=env.str("REDIS_HOST"),
            password=env.str("REDIS_PASSWORD"),
            port=env.str("REDIS_PORT")
        ),
        db=DbConfig(
            host=env.str('POSTGRES_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB'),
            port=env.str('POSTGRES_PORT'),
            URL=f"postgresql+asyncpg://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}/{env.str('POSTGRES_DB')}"
        ),
    )
