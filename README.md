# 待办事项管理器 v2.0

基于 FastAPI + 原生 JavaScript 的现代化 Web 应用。

## 功能特性

- ✅ 添加任务（支持设置优先级）
- ✅ 删除任务
- ✅ 标记完成/未完成
- ✅ 搜索任务
- ✅ 数据持久化（SQLite 数据库）
- ✅ 现代化 UI 设计

## 项目结构

```
todo-app/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── main.py       # API 入口
│   │   ├── models.py     # 数据库模型
│   │   ├── schemas.py    # 数据验证
│   │   ├── crud.py       # 数据库操作
│   │   └── database.py   # 数据库连接
│   └── requirements.txt
├── frontend/             # 前端界面
│   ├── index.html        # 主页面
│   ├── app.js            # 前端逻辑
│   └── styles.css        # 样式
├── migrate.py            # 数据迁移脚本
├── start.py              # 启动脚本
└── todo.py (旧)          # 原 tkinter 版本（已废弃）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

### 2. 启动服务

```bash
python start.py
```

或使用以下命令分别启动：

```bash
# 启动后端
cd backend
uvicorn app.main:app --reload

# 在浏览器中打开前端
open frontend/index.html
```

### 3. 数据迁移（可选）

如果需要将旧版本 tasks.json 的数据迁移到数据库：

```bash
python migrate.py
```

## API 文档

启动后端后访问：http://localhost:8000/docs

### API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/tasks` | 获取所有任务（支持 `?search=关键词`） |
| POST | `/tasks` | 创建任务 |
| PUT | `/tasks/{id}` | 更新任务 |
| DELETE | `/tasks/{id}` | 删除任务 |

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: HTML5 + TailwindCSS + 原生 JavaScript
- **架构**: 前后端分离，RESTful API
