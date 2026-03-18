# Render 部署指南

## 快速部署步骤

### 1. 创建 Render 账号
访问 https://dashboard.render.com/ 注册账号（可用 GitHub 账号登录）

### 2. 创建 PostgreSQL 数据库
1. 点击 "New +" → "PostgreSQL"
2. Name: `todo-db`
3. Database: `todo_db`
4. User: `todo_user`
5. Region: 选离你近的（如 Singapore 或 Oregon）
6. 点击 "Create Database"
7. 等待创建完成，复制 **Internal Database URL**

### 3. 部署后端 API
1. 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置：
   - Name: `todo-api`
   - Runtime: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 添加环境变量：
   - Key: `DATABASE_URL`
   - Value: 刚才复制的 PostgreSQL URL（格式：`postgresql://todo_user:xxx@host:5432/todo_db`）
5. 点击 "Create Web Service"

### 4. 部署前端
1. 点击 "New +" → "Static Site"
2. 选择同一个仓库
3. 配置：
   - Name: `todo-frontend`
   - Build Command: `echo "Frontend ready"`
   - Publish Directory: `frontend`
4. 点击 "Create Static Site"

### 5. 修改前端 API 地址（关键步骤）
前端部署完成后，需要修改 `frontend/app.js` 中的 API URL：

```javascript
const API_URL = 'https://你的后端域名.onrender.com';
```

然后提交代码，Render 会自动重新部署前端。

### 6. 配置 CORS（后端）
修改 `backend/app/main.py` 中的 CORS 配置，添加前端域名：

```python
allow_origins=[
    "https://你的前端域名.onrender.com",
    "http://localhost:8000",  # 本地开发
]
```

提交代码后后端会自动重新部署。

---

## 简化方案：只部署后端

如果不想分开部署前后端，可以把前端文件放在后端 serving：

1. 修改 `backend/app/main.py`，添加静态文件服务：
```python
from fastapi.staticfiles import StaticFiles

# 挂载前端静态文件
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
```

2. 在 Render 只创建一个 Web Service，同时跑后端和前端

---

## 常见问题

### 数据库迁移
首次部署后需要创建表，可以在本地运行：
```bash
cd backend
export DATABASE_URL="你的 PostgreSQL URL"
python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
```

或者在 Render 的 Shell 中运行。

### 免费额度限制
- Web Service: 每月 750 小时（足够 24x7 运行一个服务）
- PostgreSQL: 免费 90 天，可续期
- 服务 15 分钟无访问会休眠，首次访问需要 30 秒左右唤醒

### 自定义域名
1. 在 Render Dashboard 点击你的服务
2. 点击 "Settings" → "Custom Domains"
3. 按提示添加你的域名
