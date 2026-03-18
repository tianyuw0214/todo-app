from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def get_tasks(db: Session, search: str = None):
    query = db.query(models.Task)
    if search:
        # 限制搜索字符串长度，防止 DoS
        search = search[:100].strip()
        if search:
            query = query.filter(models.Task.text.contains(search))
    return query.order_by(models.Task.created_at.desc()).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate):
    try:
        db_task = models.Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception:
        db.rollback()
        raise


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            update_data = task_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            db.commit()
            db.refresh(db_task)
        return db_task
    except Exception:
        db.rollback()
        raise


def delete_task(db: Session, task_id: int):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
        return db_task
    except Exception:
        db.rollback()
        raise
