from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

PriorityType = Literal["高", "中", "低"]


class TaskBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="任务内容")
    done: bool = False
    priority: PriorityType = "中"

    @validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('任务内容不能为空')
        return v.strip()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=500)
    done: Optional[bool] = None
    priority: Optional[PriorityType] = None

    @validator('text')
    @classmethod
    def text_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('任务内容不能为空')
            return v.strip()
        return v


class Task(TaskBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
