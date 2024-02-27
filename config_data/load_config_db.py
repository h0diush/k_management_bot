from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class ConnectionDB:
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: int


@dataclass
class ConfigDB:
    db: ConnectionDB


def load_config_db(path: Union[str] = None) -> ConfigDB:
    env = Env()
    env.read_env(path)
    return ConfigDB(db=ConnectionDB(
        db_name=env("DB_NAME"),
        db_pass=env("DB_PASS"),
        db_user=env("DB_USER"),
        db_host=env("DB_HOST"),
        db_port=env("DB_PORT"),
    ))