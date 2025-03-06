from dataclasses import dataclass
from environs import Env
from sqlalchemy import URL
from typing import Optional


@dataclass
class DB:
    username: str
    password: str
    host: str
    port: int
    database: str

    def create_database_url(self, driver: str = "asyncpg"):
        url = URL.create(
            drivername="postgresql+"+driver,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )

        return url.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        username = env.str("POSTGRES_USER")
        password = env.str("POSTGRES_PASSWORD")
        host = env.str("POSTGRES_HOST")
        port = env.str("POSTGRES_PORT")
        database = env.str("POSTGRES_DB")

        return DB(username=username, password=password, host=host, port=port, database=database)


@dataclass
class Redis:
    host: str
    port: int

    @staticmethod
    def from_env(env: Env):
        host = env.str("REDIS_HOST")
        port = env.str("REDIS_PORT")
        return Redis(host=host, port=port)


@dataclass
class TgBot:
    token: str

    @classmethod
    def from_env(cls, env: Env):
        print(env.dump())
        token = env.str("BOT_TOKEN")
        return TgBot(token=token)


@dataclass
class Config:
    tg_bot: TgBot
    db: Optional[DB]
    redis: Optional[Redis]


def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)

    config = Config(
        tg_bot=TgBot.from_env(env),
        db=DB.from_env(env),
        redis=Redis.from_env(env)
    )

    return config
