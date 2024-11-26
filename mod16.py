from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/users")
async def get_users() -> List[User]:
    return users

@app.post("/user/{username}/{age}")
async def post_user(username: str = Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser"),
               age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> User:
    users.append(User)
    user_id = max(users, key=lambda x: int(x.id)).id if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: int = Path(ge=1, le=100, description="Enter User ID", example="20"),
        username: str = Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser"),
        age: int = Path(ge=18, le=120, description="Enter your age", example="22")):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example="20")):
    for j in users:
        if j.id == user_id:
            users.remove(user_id)
            return j
    raise HTTPException(status_code=404, detail="User was not found")

#uvicorn mod16:app