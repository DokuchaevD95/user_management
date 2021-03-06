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
        """
        Метод получения пользвоателя по логину
        :param login:
        :return:
        """
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
        """
        Метод получения пользователя по ID
        :param id_:
        :return:
        """
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
        """
        Получение списка пользователей. Пагинация не предусмотрена
        :return:
        """
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
        """
        Метод удаления пользвоателя.
        Реализовано по принципу Soft Delete
        Физически из базы пользователь не удаляется!
        :param id_:
        :return:
        """
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
        """
        Создание пользователя с проверкой на
        существование логина
        :param user:
        :return:
        """
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

    async def update(self, user_id: int, user: UserModel) -> UserModel:
        """
        Обновление пользователя. Не запрещается обновление
        логина, но логин должен быть уникальным
        :param user_id:
        :param user:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                statement = select(UserOrm).where(
                    UserOrm.id == user_id
                )
                user_orm = await session.scalar(statement)
                user_with_same_login = await self.get_by_login(user.login)

                if user_with_same_login and user_id != user_with_same_login.id:
                    raise HTTPException(400, detail='Login already in use')

                fields = user.dict(exclude={'created_at', 'id'})
                for key, value in fields.items():
                    setattr(user_orm, key, value)

                session.add(user_orm)
                await session.commit()
                return UserModel.from_orm(user_orm)

