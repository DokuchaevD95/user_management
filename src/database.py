"""Файл создающий и экспортирующий engine подключения к ДБ"""

__all__ = ['engine', 'async_session']

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import config


db_config = config['database']
URL = f'{db_config["drivername"]}://' \
      f'{db_config["username"]}:' \
      f'{db_config["password"]}@' \
      f'{db_config["host"]}:{db_config["port"]}/' \
      f'{db_config["dbname"]}'

# Асинхронные engine и фабрика сессий SQLAlchemy
engine = create_async_engine(URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
