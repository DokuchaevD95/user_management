"""Создает первого пользователя с полным доступом"""

__all__ = ['seed']

from datetime import datetime
from sqlalchemy import text

from database import engine
from models import BaseOrm


async def seed():
    statement = f"""
        INSERT INTO users (login, password, last_name, first_name, is_admin, created_at)
        SELECT 'admin', 'admin', 'Системный', 'Пользователь', TRUE, '{datetime.now()}'
        WHERE NOT EXISTS (
            SELECT id FROM users WHERE id = 1
        );
    """

    # Реализовано в try из за docker-compose
    # слишком долго открывается порт либо инциализируется docker network
    conn = None
    while not conn:
        try:
            conn = await engine.begin()
        except ConnectionRefusedError:
            pass

    await conn.run_sync(BaseOrm.metadata.create_all)
    await conn.execute(text(statement))
    await conn.commit()

    await conn.close()
