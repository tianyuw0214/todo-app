# Render 部署指南

## 快速部署步骤

前后端已合并部署，只需创建一个 Web Service。

### 1. 创建 Render 账号
访问 https://dashboard.render.com/ 注册账号（可用 GitHub 账号登录）

### 2. 创建 PostgreSQL 数据库
1. 点击 "New +" → "PostgreSQL"
2. Name: `todo-db`
3. Database: `todo_db`
4. User: `todo_user`
5. Region: 选离你近的（如 Singapore 或 Oregon）
6. 点击 "Create Database"
7. 等待创建完成（约 1-2 分钟）

### 3. 部署应用
1. 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置：
   - Name: `todo-app`（或你喜欢的名字）
   - Runtime: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 环境变量会自动从 `render.yaml` 读取，如果没有：
   - 添加 `DATABASE_URL`，值从 PostgreSQL 页面复制
5. 点击 "Create Web Service"

### 4. 等待部署完成
- 构建过程约 2-3 分钟
- 部署完成后，会给你一个域名如 `https://todo-app-xxx.onrender.com`
- 直接访问这个域名即可使用完整应用

---

## 架构说明

合并部署后：
- `https://你的域名/` → 前端页面（HTML/CSS/JS）
- `https://你的域名/api/tasks` → API 端点
- `https://你的域名/api/` → API 信息

不需要处理 CORS，因为前后端在同域名下。

---

## 常见问题

### 数据库迁移
首次部署后需要创建表，可以在 Render Shell 中运行：
```bash
cd backend
python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
```

### 免费额度限制
- Web Service: 每月 750 小时（足够 24x7 运行一个服务）
- PostgreSQL: 免费 90 天，可续期
- 服务 15 分钟无访问会休眠，首次访问需要 30 秒左右唤醒

### 自定义域名
1. 在 Render Dashboard 点击你的服务
2. 点击 "Settings" → "Custom Domains"
3. 按提示添加你的域名
