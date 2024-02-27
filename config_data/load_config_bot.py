from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class ConfigBot:
    tg_bot: TgBot


def load_config_tg_bot(path: Union[str] = None) -> ConfigBot:
    env = Env()
    env.read_env(path)
    return ConfigBot(tg_bot=TgBot(token=env("BOT_TOKEN")))
