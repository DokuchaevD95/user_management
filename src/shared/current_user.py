"""Метод с получением пользователья по токену"""

__all__ = ["get_curr_user"]

from fastapi import Cookie
from typing import Optional
from jwt import decode as jwt_decode

from config import config
from models import UserModel


def get_curr_user(token: Optional[str] = Cookie(None)) -> Optional[UserModel]:
    """
    Энкодирует токен, полученный в cookie
    и создает Pydantic модель текущего пользователя
    :param token:
    :return:
    """
    if token:
        user_content = jwt_decode(token, key=config['jwt_secret'], algorithms=config['jwt_alg'])
        curr_user = UserModel(**user_content)
        return curr_user
    return None
