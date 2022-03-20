"""Контроллеры по пользователю"""

__all__ = ['user_router']

from jwt import decode as jwt_decode
from typing import Optional
from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from config import config
from models import UserModel
from services.user import UserService
from shared.jinja import jinja_env


user_router = APIRouter(prefix='/users')


def check_auth(token: Optional[str] = Cookie(None)) -> Optional[UserModel]:
    if token:
        user_content = jwt_decode(token, key=config['jwt_secret'], algorithms='HS256')
        curr_user = UserModel(**user_content)
        return curr_user
    return None


@user_router.get('/list')
async def render_users_list(user_service: UserService = Depends(UserService),
                            curr_user: Optional[UserModel] = Depends(check_auth)
                            ) -> Response:
    if not curr_user:
        return RedirectResponse('/auth')

    users = await user_service.fetch()
    template = jinja_env.get_template('html/user-list.html')
    content = await template.render_async(
        curr_user=curr_user,
        users=users
    )
    return HTMLResponse(status_code=200, content=content)


@user_router.get('/delete/{user_id}')
async def delete_user(user_id: int,
                      curr_user: Optional[UserModel] = Depends(check_auth),
                      user_service: UserService = Depends(UserService)
                      ) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/list')

    await user_service.delete(user_id)
    return RedirectResponse('/list')


@user_router.get('/create')
async def render_user_create(curr_user: Optional[UserModel] = Depends(check_auth)) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/list')

    template = jinja_env.get_template('html/user-create.html')
    content = await template.render_async()
    return HTMLResponse(status_code=200, content=content)


@user_router.get('/save')
async def save_user(curr_user: Optional[UserModel] = Depends(check_auth),
                    user_service: UserService = Depends(UserService)
                    ) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/list')

    template = jinja_env.get_template('html/user-create.html')
    content = await template.render_async()
    return HTMLResponse(status_code=200, content=content)
