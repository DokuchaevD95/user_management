"""Контроллеры с авторизацией"""

__all__ = ['auth_router']

import json

from jwt import encode as jwt_encode
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from config import config
from services.user import UserService
from shared.jinja import jinja_env


auth_router = APIRouter()


class AuthParams(BaseModel):
    login: str
    password: str


@auth_router.get('/auth')
async def render_auth_page() -> Response:
    template = jinja_env.get_template('html/auth.html')
    content = await template.render_async()
    return HTMLResponse(content)


@auth_router.post('/auth')
async def check_auth(params: AuthParams, user_service: UserService = Depends(UserService)) -> Response:
    user = await user_service.get_by_login(params.login)
    if user and user.password == params.password:
        content = user.json(exclude={'password'})
        content = json.loads(content)
        content['token'] = jwt_encode(content, config['jwt_secret'], algorithm='HS256')
        return JSONResponse(content=content)

    return Response(status_code=401, content='Incorrect login or passwd was passed')


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
