# Валидация данных
# Задача "Аннотация и валидация":

from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get("/user/admin")
async def admin() -> str:
    return "Вы вошли как администратор"


@app.get("/user/{username}/{age}")
async def user_info(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                  examples="UrbanUser")],
               age: int = Path(ge=18, le=120, description="Enter age", examples=24)) -> str:
    return f"Информация о пользователе. Имя: {username}, возраст: {age}"


@app.get("/user/{user_id}")
async def usid(user_id: int = Path(ge=1, le=100,description="Enter User ID", examples=1)) -> str:
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/")
async def welcom() -> str:
    return "Главная страница"
