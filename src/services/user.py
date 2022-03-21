"""Сервис по работе с пользователем и БД"""

__all__ = ['UserService']

from datetime import datetime
from sqlalchemy import select
from typing import Optional, List
from fastapi import HTTPException

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
            if not user:
                return None
            return UserModel.from_orm(user)

    @staticmethod
    async def get(id_: int) -> Optional[UserModel]:
        async with async_session() as session:
            statement = select(UserOrm).where(
                UserOrm.id == id_,
                UserOrm.deleted_at.is_(None)
            )
            user = await session.scalar(statement)
            if not user:
                raise HTTPException(status_code=404, detail='User not found')
            return user

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
                user: UserOrm = await session.scalar(statement)
                if not user:
                    raise HTTPException(status_code=404, detail='User not found')

                user.deleted_at = datetime.now()
                session.add(user)
                await session.commit()

                return UserModel.from_orm(user)

    @staticmethod
    async def create(user: UserModel) -> UserModel:
        async with async_session() as session:
            async with session.begin():
                user_orm = UserOrm(**user.dict())

                statement = select(UserOrm).where(
                    UserOrm.login == user.login.lower()
                )
                if await session.scalar(statement):
                    raise HTTPException(status_code=400, detail='Login already in use')

                session.add(user_orm)
                await session.commit()
                return UserModel.from_orm(user_orm)

    @staticmethod
    async def update(user_id: int, user: UserModel) -> UserModel:
        async with async_session() as session:
            async with session.begin():
                statement = select(UserOrm).where(
                    UserOrm.login == user.login.lower()
                )
                if await session.scalar(statement):
                    raise HTTPException(status_code=400, detail='Login already in use')

                statement = select(UserOrm).where(
                    UserOrm.id == user_id
                )
                user_orm = await session.scalar(statement)
                fields = user.dict(exclude={'created_at', 'id'})
                for key, value in fields.items():
                    setattr(user_orm, key, value)

                session.add(user_orm)
                await session.commit()
                return UserModel.from_orm(user_orm)

