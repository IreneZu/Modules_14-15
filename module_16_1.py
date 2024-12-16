# Основы Fast Api и маршрутизация
# Задача "Начало пути":

from fastapi import FastAPI

app = FastAPI()

@app.get("/user/admin")
async def welcom() -> str:
    return "Вы вошли как администратор"


@app.get("/user/{user_id}")
async def usid(user_id: str) -> str:
    return f"Вы вошли как пользователь № {user_id}"


@app.get("/user")
async def user_info(username: str="III", age: int = 18) -> str:
    return f"Информация о пользователе. Имя: {username}, возраст: {age}"
#   /user?username=Irene&age=11

@app.get("/")
async def welcom() -> str:
    return "Главная страница"

#   python3 -m uvicorn main:app
#   uvicorn main:app --
#   http://127.0.0.1:8000
