from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config_data import ConfigDB, config_db


def get_url_from_db() -> URL:
    db_data: ConfigDB = config_db()
    url = URL.create(
        "postgresql+asyncpg",
        username=db_data.db.db_user,
        password=db_data.db.db_pass,
        database=db_data.db.db_name,
        host=db_data.db.db_host,
        port=db_data.db.db_port,
    )
    return url


engine = create_async_engine(url=get_url_from_db(), echo=True)
async_session = async_sessionmaker(engine)
