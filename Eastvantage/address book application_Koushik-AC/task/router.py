from fastapi import APIRouter, Request, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from typing import List

import db

from . import schema
from .import services

router = APIRouter(
    tags=['Tasks'],
    prefix='/tasks'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task(request: schema.TaskBase,
                         database: Session = Depends(db.get_db)):

    task = await services.create_new_task(request, database)
    return task


@router.post('/bulk', status_code=status.HTTP_201_CREATED)
async def create_task_bulk(request: schema.TaskList,
                         database: Session = Depends(db.get_db)):
    
    tasks = await services.create_bulk_task_upload(request.data, database)

    return tasks


@router.get('/', response_model=List[schema.TaskBase])
async def get_all_tasks(database: Session = Depends(db.get_db)):
    return await services.get_all_tasks(database)


@router.get('/{task_id}', status_code=status.HTTP_200_OK, response_model=schema.TaskBase)
async def get_task_by_id(task_id: int, database: Session = Depends(db.get_db)):
    return await services.get_task_by_id(task_id, database)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task_by_id(task_id: int,
                                database: Session = Depends(db.get_db)):
    return await services.delete_task_by_id(task_id, database)


@router.patch('/{task_id}', status_code=status.HTTP_200_OK, response_model=schema.TaskBase)
async def update_task_by_id(task_id: int, request: schema.TaskUpdate, database: Session = Depends(db.get_db)):
    return await services.update_task_by_id(task_id, request, database)
