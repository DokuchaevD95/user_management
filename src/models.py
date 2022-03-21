"""Файл с моделями sqlalchemy"""

__all__ = [
    'BaseOrm',
    'UserOrm',
    'UserModel'
]


from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    DateTime
)


BaseOrm = declarative_base()


class UserOrm(BaseOrm):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(Text, nullable=False, unique=True, default='')
    password = Column(Text, nullable=False, default='')
    last_name = Column(Text, nullable=False, default='')
    first_name = Column(Text, nullable=False, default='')
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True, default=None)


class UserModel(BaseModel):
    id: Optional[int]
    login: str
    password: Optional[str]
    last_name: str
    first_name: str
    is_admin: bool = False
    created_at: datetime = datetime.now()
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda item: str(item)
        }
