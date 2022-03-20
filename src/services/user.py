"""Сервис по работе с пользователем и БД"""

__all__ = ['UserService']

from datetime import datetime
from sqlalchemy import select
from typing import Optional, List

from database import async_session
from models import UserModel, UserOrm


class UserService:
    @staticmethod
    async def get_by_login(login: str) -> Optional[UserModel]:
        async with async_session() as session:
            statement = select(UserOrm).where(
                UserOrm.login == login,
                UserOrm.deleted_at.is_(None)
            )
            user = await session.scalar(statement)
            if user:
                return UserModel.from_orm(user)
            return None

    @staticmethod
    async def get(id_: int) -> Optional[UserModel]:
        async with async_session() as session:
            statement = select(UserOrm).where(
                UserOrm.id == id_,
                UserOrm.deleted_at.is_(None)
            )
            user = await session.scalar(statement)
            if user:
                return UserModel.from_orm(user)
            return None

    @staticmethod
    async def fetch() -> List[UserModel]:
        async with async_session() as session:
            statement = select(UserOrm).where(
                UserOrm.deleted_at.is_(None)
            )
            result = await session.execute(statement)
            users = []
            for user in result.scalars():
                users.append(UserModel.from_orm(user))
            return users

    @staticmethod
    async def delete(id_: int) -> Optional[UserModel]:
        async with async_session() as session:
            async with session.begin():
                statement = select(UserOrm).where(
                    UserOrm.id == id_
                )
                user: UserOrm = await session.execute(statement)
                if not user:
                    return None
                user.deleted_at = datetime.now()
                session.add(user)
                await session.commit()

                return UserModel.from_orm(user)

    @staticmethod
    async def create(user: UserModel) -> UserModel:
        async with async_session() as session:
            async with session.begin():
                user_orm = UserOrm(**user.json())
                session.add(user_orm)
                await session.commit()

                return UserModel.from_orm(user_orm)
