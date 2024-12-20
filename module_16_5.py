# Шаблонизатор Jinja 2
# Задача "Список пользователей в шаблоне":

from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str = ""
    age: int = 0


@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    for user_ in users:
        if user_.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user_})

    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def post_user(username: str = Path(min_length=5, max_length=20, description="Enter username"),
                    age: int = Path(ge=18, le=120, description="Enter age")) -> User:
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id)
    new_user.username = username
    new_user.age = age
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int = Path(ge=1, le=100, description="Enter User ID"),
                      username: str = Path(min_length=5, max_length=20, description="Enter username"),
                      age: int = Path(ge=18, le=120, description="Enter age")) -> User:
    for user_ in users:
        if user_.id == user_id:
            user_.username = username
            user_.age = age
            return user_
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID")) -> User:
    for i, user_ in enumerate(users):
        if user_.id == user_id:
            #user_removed = (
            users.pop(i)
            return user_

    raise HTTPException(status_code=404, detail="User not found")
