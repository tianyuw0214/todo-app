# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

待办事项管理器 (Todo App) - 一个纯前端的待办事项 Web 应用。

- **类型**: 纯前端静态网页应用
- **存储**: 浏览器 localStorage
- **架构**: 单页面应用，无需后端

## Development

### 本地预览

直接打开 `index.html` 即可，或使用本地服务器：

```bash
python -m http.server 8000
```

### 项目结构

```
todo-app/
├── index.html   # 主页面，包含 HTML 结构和内联样式
├── app.js       # 前端逻辑：localStorage 操作、DOM 操作、事件处理
├── styles.css   # 样式文件（当前内联在 HTML 中，可提取）
├── README.md    # 项目说明
└── DEPLOY.md    # 部署指南
```

### 核心功能实现

**数据存储 (app.js)**:
```javascript
const STORAGE_KEY = 'todo-app-tasks';

// 从 localStorage 加载
function loadTasksFromStorage() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
}

// 保存到 localStorage
function saveTasksToStorage(tasks) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

// 生成 ID
function generateId() {
    return Date.now();
}
```

**任务数据结构**:
```javascript
{
    id: number,              // 时间戳生成的唯一 ID
    text: string,            // 任务内容
    done: boolean,           // 是否完成
    priority: '高'|'中'|'低', // 优先级
    created_at: ISOString,   // 创建时间
    updated_at: ISOString    // 更新时间
}
```

## 重要文件

- `app.js` - 核心逻辑，修改功能从这里开始
- `index.html` - UI 结构，样式内联在 `<style>` 标签中

## 部署

支持任何静态托管服务：
- GitHub Pages（推荐，免费）
- Netlify（拖拽部署）
- Vercel（自动部署）
- 腾讯云 COS / 阿里云 OSS

详见 `DEPLOY.md`

## 浏览器限制

- localStorage 容量限制：约 5-10MB
- 数据绑定到特定域名
- 清除浏览器数据会导致任务丢失
- 每个用户的数据独立存储

## 遗留代码

- `todo.py.bak` - 原 tkinter 桌面版本（如存在可删除）
- `backend/` - 原 Flask 后端（已删除）
