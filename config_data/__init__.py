__all__ = ["config_bot", "ConfigBot", "config_db", "ConfigDB"]

from config_data.load_config_bot import ConfigBot
from config_data.load_config_bot import load_config_tg_bot as config_bot
from config_data.load_config_db import ConfigDB
from config_data.load_config_db import load_config_db as config_db
