# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

待办事项管理器 (Todo App) - 一个前后端分离的 Web 应用，用于管理日常任务。

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: 原生 HTML/CSS/JavaScript (无构建工具)
- **架构**: RESTful API，前端通过 fetch 调用后端

## Development Commands

### Start Development Server

```bash
# 启动后端 (前台运行)
cd backend && python -m uvicorn app.main:app --reload --port 8000

# 或使用启动脚本 (同时启动后端并保持运行)
python start.py
```

后端启动后：
- API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 前端页面: 直接打开 `frontend/index.html`

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Data Migration

```bash
# 将旧版 tasks.json 数据迁移到 SQLite
python migrate.py
```

## Architecture

### Backend Structure (`backend/app/`)

```
backend/
├── app/
│   ├── main.py       # FastAPI 路由定义，API 入口
│   ├── models.py     # SQLAlchemy 数据库模型 (Task)
│   ├── schemas.py    # Pydantic 数据验证模型
│   ├── crud.py       # 数据库 CRUD 操作封装
│   └── database.py   # SQLite 连接和 Session 管理
├── requirements.txt
└── todos.db          # SQLite 数据库文件 (自动生成)
```

**Key Architecture Points:**
- 使用 SQLAlchemy ORM 进行数据库操作
- 数据库文件 `todos.db` 自动生成在 backend 目录
- CORS 已配置为允许所有来源 (`allow_origins=["*"]`)，方便本地开发

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks` | 获取所有任务，支持 `?search=关键词` 搜索 |
| POST | `/tasks` | 创建新任务 |
| PUT | `/tasks/{id}` | 更新任务 (标记完成/修改内容) |
| DELETE | `/tasks/{id}` | 删除任务 |

### Frontend Structure

```
frontend/
├── index.html   # 单页面应用，包含所有 HTML 结构
├── app.js       # 前端逻辑：API 调用、DOM 操作、事件处理
└── styles.css   # 样式文件 (可选，当前内联在 HTML 中)
```

**Key Points:**
- 前端是静态文件，直接浏览器打开即可
- 需要后端运行在 localhost:8000
- 使用原生 fetch API 与后端通信

## Database Schema

**Task 表:**
- `id`: Integer, Primary Key
- `text`: String, 任务内容
- `done`: Boolean, 是否完成
- `priority`: String, 优先级 (高/中/低)
- `created_at`: DateTime, 创建时间
- `updated_at`: DateTime, 更新时间

## Important Files

- `backend/app/main.py` - API 路由，添加新端点在这里
- `backend/app/models.py` - 数据库模型，修改表结构需要删除 todos.db 重新生成
- `frontend/app.js` - 前端逻辑，API 基础 URL: `http://localhost:8000`
- `migrate.py` - 从旧版 JSON 数据迁移到数据库

## Legacy Code

- `todo.py.bak` - 原 tkinter 桌面版本 (已废弃，保留作参考)
- `tasks.json` - 旧版数据文件，可用 migrate.py 迁移
