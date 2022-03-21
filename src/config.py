"""Файл, читающий конфиг json и предоставляющий объект конфига на экспорт"""

__all__ = ['config']

import os

config = {
  'database': {
    'drivername': 'postgresql+asyncpg',
    'dbname': 'user_management',
    'port': 5432,
    'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
    'username': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', '3LdNmrGS')
  },
  'jwt_secret': '214sdfg345dew4r2',
  'jwt_alg': 'HS256'
}
