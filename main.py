from fastapi import FastAPI
from routers import task, user

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

#В файле main.py создайте сущность FastAPI(), напишите один маршрут для неё - '/',
#по которому функция возвращает словарь - {"message": "Welcome to Taskmanager"}.
#Импортируйте объекты APIRouter и подключите к ранее созданному приложению FastAPI,
#объединив все маршруты в одно приложение.

#uvicorn main:app
#alembic init migration
#alembic revision --autogenerate
#uvicorn main:app
