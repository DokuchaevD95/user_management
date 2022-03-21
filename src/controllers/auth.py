"""Контроллеры с авторизацией"""

__all__ = ['auth_router']

import json

from jwt import encode as jwt_encode
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from config import config
from models import UserModel
from services.user import UserService
from shared.jinja import jinja_env
from shared.current_user import get_curr_user


auth_router = APIRouter()


class AuthParams(BaseModel):
    login: str
    password: str


@auth_router.get('/')
@auth_router.get('/auth')
async def render_auth_page(curr_user: Optional[UserModel] = Depends(get_curr_user)) -> Response:
    if curr_user:
        return RedirectResponse('/users/list')

    template = jinja_env.get_template('html/auth.html')
    content = await template.render_async()
    return HTMLResponse(content)


@auth_router.post('/auth')
async def check_auth(params: AuthParams, user_service: UserService = Depends(UserService)) -> Response:
    user = await user_service.get_by_login(params.login)
    if user and user.password == params.password:
        content = user.json(exclude={'password'})
        content = json.loads(content)
        content['token'] = jwt_encode(content, config['jwt_secret'], algorithm=config['jwt_alg'])
        return JSONResponse(content=content)

    raise HTTPException(status_code=401, detail='Incorrect login or passwd was passed')


@auth_router.get('/auth/ok')
async def save_auth_token(jwt: Optional[str] = '') -> Response:
    response = RedirectResponse('/users/list')
    response.set_cookie(key='token', value=jwt)
    return response


@auth_router.get('/logout')
async def logout() -> Response:
    response = RedirectResponse('/auth')
    response.delete_cookie('token')
    return response
