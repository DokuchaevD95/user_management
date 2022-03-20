"""Файл, читающий конфиг json и предоставляющий объект конфига на экспорт"""

__all__ = ['config']

config = {
  'database': {
    'drivername': 'postgresql+asyncpg',
    'dbname': 'user_management',
    'port': 5432,
    'host': '127.0.0.1',
    'username': 'admin',
    'password': '3LdNmrGS'
  },
  'jwt_secret': '214sdfg345dew4r2'
}
