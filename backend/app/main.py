import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="待办事项 API", version="2.0")

# CORS 配置
# 注意：生产环境应该限制具体的来源，不要在生产环境使用 allow_origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境使用，生产环境应改为具体域名如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def read_root():
    return {"message": "待办事项 API 运行中", "version": "2.0"}


@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(search: str = None, db: Session = Depends(get_db)):
    logger.info(f"获取任务列表, 搜索关键词: {search}")
    tasks = crud.get_tasks(db, search=search)
    return tasks


@app.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"创建新任务: {task.text[:50]}...")
    return crud.create_task(db, task)


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"更新任务 {task_id}: {task.model_dump(exclude_unset=True)}")
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return db_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"删除任务 {task_id}")
    db_task = crud.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return None
