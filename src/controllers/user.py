"""Контроллеры по пользователю"""

__all__ = ['user_router']

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from models import UserModel
from services.user import UserService
from shared.jinja import jinja_env
from shared.current_user import get_curr_user


user_router = APIRouter(prefix='/users')


@user_router.get('/list')
async def render_users_list_page(user_service: UserService = Depends(UserService),
                                 curr_user: Optional[UserModel] = Depends(get_curr_user)
                                 ) -> Response:
    """
    Рендер списка пользователя
    :param user_service:
    :param curr_user:
    :return:
    """
    if not curr_user:
        return RedirectResponse('/auth')

    users = await user_service.fetch()
    template = jinja_env.get_template('html/user-list.html')
    content = await template.render_async(
        curr_user=curr_user,
        users=users
    )
    return HTMLResponse(content=content)


@user_router.get('/create')
async def render_user_create_page(curr_user: Optional[UserModel] = Depends(get_curr_user)) -> Response:
    """
    Рендер страницы создания пользователя
    :param curr_user:
    :return:
    """
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list')

    template = jinja_env.get_template('html/user-create.html')
    content = await template.render_async()
    return HTMLResponse(content=content)


@user_router.get('/edit/{user_id}')
async def render_user_edit_page(user_id: int,
                                curr_user: Optional[UserModel] = Depends(get_curr_user),
                                user_service: UserService = Depends(UserService)
                                ) -> Response:
    """
    Контроллер отдает страницу редактирования пользователя.
    Предусмотрена подгрузка всех текущих данных
    :param user_id:
    :param curr_user:
    :param user_service:
    :return:
    """
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
    """
    Контроллер удаление пользователя.
    Текущего пользователя (себя) удалить нельзя
    :param user_id:
    :param curr_user:
    :param user_service:
    :return:
    """
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list')

    if curr_user.id == user_id:
        raise HTTPException(status_code=400, detail='You cannot delete yourself')

    await user_service.delete(user_id)
    return RedirectResponse('/users/list', status_code=302)


@user_router.post('/create', response_model=UserModel)
async def save_user(user: UserModel,
                    curr_user: Optional[UserModel] = Depends(get_curr_user),
                    user_service: UserService = Depends(UserService)):
    """
    Контроллер создание пользователя
    :param user:
    :param curr_user:
    :param user_service:
    :return:
    """
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list', status_code=302)

    user = await user_service.create(user)
    return user


@user_router.post('/edit/{user_id}', response_model=UserModel)
async def edit_user(user_id: int,
                    user: UserModel,
                    curr_user: Optional[UserModel] = Depends(get_curr_user),
                    user_service: UserService = Depends(UserService)):
    """
    Контроллер реджактиррвоания пользователя.
    Если редактрруется текущий авторизованный пользователь
    (логин, пароль, права), то его разлогинит
    :param user_id:
    :param user:
    :param curr_user:
    :param user_service:
    :return:
    """
    if not curr_user or not curr_user.is_admin:
        return RedirectResponse('/users/list', status_code=302)

    user = await user_service.update(user_id, user)
    logout_condition = [
        user.password != curr_user.password,
        user.is_admin != curr_user.is_admin,
        user.login != curr_user.login
    ]
    if user.id == curr_user.id and any(logout_condition):
        return RedirectResponse('/logout', status_code=302)
    return user
