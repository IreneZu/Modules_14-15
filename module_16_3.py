from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

'''@app.get("/")
async def welcom() -> str:
    return "Главная страница"
'''

@app.get("/users")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: str = Path(min_length=5, max_length=20, description="Enter username"),
                    age: int = Path(ge=18, le=120, description="Enter age")) -> str:
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered."


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str = Path(min_length=1, max_length=3, regex="^[0-9]+$", description="Enter User ID"),
                      username: str = Path(min_length=5, max_length=20, description="Enter username"),
                      age: int = Path(ge=18, le=120, description="Enter age")) -> str:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} has been updated."


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: str = Path(min_length=1, max_length=3, regex="^[0-9]+$", description="Enter User ID")) -> str:
    users.pop(user_id)
    return f"User {user_id} has been deleted."
