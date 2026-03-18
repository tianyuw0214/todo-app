# 待办事项管理器

纯前端待办事项应用，使用浏览器 localStorage 存储数据。

## 功能特性

- 添加任务（支持设置优先级：高/中/低）
- 标记完成/未完成
- 删除任务
- 筛选任务（全部/进行中/已完成）
- 数据持久化（浏览器 localStorage）
- 编辑风格 UI 设计

## 项目结构

```
todo-app/
├── index.html    # 主页面
├── app.js        # 前端逻辑
├── styles.css    # 样式文件
└── README.md     # 项目说明
```

## 快速开始

直接在浏览器中打开 `index.html` 即可使用，无需安装任何依赖或启动服务器。

### 本地开发

```bash
# 使用任意本地服务器（可选）
# Python 3
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

然后访问 http://localhost:8000

## 数据存储

- 数据保存在浏览器的 localStorage 中
- 每个用户的数据独立存储在自己的浏览器中
- 清除浏览器数据会导致任务丢失
- 存储限制约为 5-10MB（足够存储数千条任务）

## 部署

支持任意静态托管服务，详见 [DEPLOY.md](DEPLOY.md)。

推荐方案：
- [GitHub Pages](https://pages.github.com/)（免费，最简单）
- [Netlify](https://www.netlify.com/)（拖拽部署）
- [Vercel](https://vercel.com/)（自动部署）

## 技术栈

- HTML5
- CSS3（原生样式，无框架）
- 原生 JavaScript（ES6+）
- localStorage API

## 浏览器支持

- Chrome / Edge / Firefox / Safari 最新版本
- 支持移动端浏览器
