from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
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
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="20")],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanProfi")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter your age", example="22")]):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter user ID", example="20")]) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")

#uvicorn module162:app