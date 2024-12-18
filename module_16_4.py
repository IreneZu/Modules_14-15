from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str = ""
    age: int = 0


@app.get("/users")
async def get_users() -> List[User]:
    return users


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
