"""Контроллеры по пользователю"""

__all__ = ['user_router']

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from models import UserModel
from services.user import UserService
from shared.jinja import jinja_env
from shared.current_user import get_curr_user


user_router = APIRouter(prefix='/users')


@user_router.get('/list')
async def render_users_list(user_service: UserService = Depends(UserService),
                            curr_user: Optional[UserModel] = Depends(get_curr_user)
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


@user_router.get('/create')
async def render_user_create(curr_user: Optional[UserModel] = Depends(get_curr_user)) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list')

    template = jinja_env.get_template('html/user-create.html')
    content = await template.render_async()
    return HTMLResponse(status_code=200, content=content)


@user_router.get('/edit/{user_id}')
async def render_user_edit(user_id: int,
                           curr_user: Optional[UserModel] = Depends(get_curr_user),
                           user_service: UserService = Depends(UserService)
                           ) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list')

    user = await user_service.get(user_id)
    template = jinja_env.get_template('html/user-edit.html')
    content = await template.render_async(user=user)
    return HTMLResponse(content=content)


@user_router.get('/delete/{user_id}')
async def delete_user(user_id: int,
                      curr_user: Optional[UserModel] = Depends(get_curr_user),
                      user_service: UserService = Depends(UserService)
                      ) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list')

    await user_service.delete(user_id)
    return RedirectResponse('/users/list', status_code=302)


@user_router.post('/save')
@user_router.post('/save/{user_id}')
async def upsert_user(user_id: Optional[int] = None,
                      login: str = Form(...),
                      password: str = Form(...),
                      first_name: str = Form(...),
                      last_name: str = Form(...),
                      is_admin: Optional[bool] = Form(False),
                      curr_user: Optional[UserModel] = Depends(get_curr_user),
                      user_service: UserService = Depends(UserService)
                      ) -> Response:
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list', status_code=302)

    user = UserModel(
        id=user_id,
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin,
        created_at=datetime.now()
    )
    await user_service.upsert(user)
    return RedirectResponse('/users/list', status_code=302)
