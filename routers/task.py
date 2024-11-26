from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from task2 import Task
from user2 import User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task)).all()
    return task


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        return task
    raise HTTPException(status_code=404, detail="Task was not found")

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      create_task_model: CreateTask, user_id: int):
    task = db.scalars(select(User).where(User.id == user_id))
    if task is not None:
        db.execute(insert(Task).values(title=create_task_model.title,
                                       content=create_task_model.content,
                                       user_id=user_id,
                                       slug=slugify(create_task_model.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

    raise HTTPException(status_code=404, detail="User was not found")



@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      update_task_model: UpdateTask, task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    for i in task:
        if i is None:
            db.execute(update(Task).where(Task.id == task_id).values(
                title=update_task_model.title,
                content=update_task_model.content,
                priority=update_task_model.priority))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

    raise HTTPException(status_code=404, detail="Tasl was not found")

@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == task_id))
    for task in tasks:
        if task is None:
            db.execute(delete(Task).where(Task.user_id == task_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}

    raise HTTPException(status_code=404, detail="User was not found")


