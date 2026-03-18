import logging
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db, init_db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 启动时自动初始化数据库
try:
    init_db()
    logger.info("数据库初始化成功")
except Exception as e:
    logger.error(f"数据库初始化失败: {e}")

app = FastAPI(title="待办事项 API", version="2.0")

# CORS 配置（合并部署后主要用于本地开发）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 合并部署后 CORS 不影响，主要用于本地开发
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# API 路由 - 所有 API 都在 /api 前缀下
api_router = FastAPI(title="待办事项 API", version="2.0")


@api_router.get("/")
def api_root():
    return {"message": "待办事项 API 运行中", "version": "2.0"}


@api_router.get("/tasks", response_model=List[schemas.Task])
def read_tasks(search: str = None, db: Session = Depends(get_db)):
    logger.info(f"获取任务列表, 搜索关键词: {search}")
    tasks = crud.get_tasks(db, search=search)
    return tasks


@api_router.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"创建新任务: {task.text[:50]}...")
    return crud.create_task(db, task)


@api_router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"更新任务 {task_id}: {task.dict(exclude_unset=True)}")
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return db_task


@api_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"删除任务 {task_id}")
    db_task = crud.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return None


# 挂载 API 路由
app.mount("/api", api_router)

# 静态文件目录路径
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")


# 如果前端目录存在，挂载静态文件
if os.path.exists(frontend_dir):
    # 先挂载静态文件目录
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def serve_root():
    """首页返回 index.html"""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "待办事项 API 运行中", "version": "2.0"}


@app.get("/{path:path}")
def serve_static(path: str):
    """其他路径尝试返回对应的静态文件，否则返回 index.html（支持前端路由）"""
    file_path = os.path.join(frontend_dir, path)
    # 如果文件存在，返回文件
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # 否则返回 index.html（让前端路由处理）
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"message": "File not found"}
