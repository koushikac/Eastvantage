from typing import Optional, List
from pydantic import BaseModel, constr


class TaskBase(BaseModel):
    id: Optional[int]
    name: str
    description: str

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class TaskList(BaseModel):
    data: List[TaskBase]
