import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from controllers import auth_router, user_router
from seed import seed


app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)


# Монтирование шаблонов / css / js в роутинг приложения
app.mount('/templates', StaticFiles(directory='templates'), name='templates')


@app.on_event('startup')
async def seed_db():
    return await seed()


if __name__ == '__main__':
    # запуск для dev разработки
    uvicorn.run(app, host='127.0.0.1', port=8000)
