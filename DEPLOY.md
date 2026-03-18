# 部署指南

本应用是纯前端静态网站，可部署到任何静态托管服务。

## 推荐方案：GitHub Pages（免费）

1. 将代码推送到 GitHub 仓库
2. 进入仓库 Settings → Pages
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "master" 或 "main"，文件夹选择 "/ (root)"
5. 点击 Save，等待几分钟
6. 访问 `https://你的用户名.github.io/仓库名`

## 备选方案

### Netlify（推荐）

1. 访问 https://app.netlify.com/drop
2. 将项目文件夹拖拽到页面上
3. 自动获得临时域名，可绑定自定义域名

### Vercel

```bash
npm i -g vercel
vercel
```

### Render Static Site

1. 访问 https://dashboard.render.com
2. 创建 Static Site
3. 连接 GitHub 仓库
4. 保持默认设置，点击部署

### Cloudflare Pages

1. 登录 Cloudflare Dashboard
2. 进入 Pages → Create a project
3. 连接 GitHub 仓库
4. 构建命令留空，输出目录留空
5. 点击保存并部署

### 腾讯云 COS / 阿里云 OSS

1. 创建存储桶，开启静态网站托管
2. 上传所有文件到存储桶
3. 配置自定义域名（可选）

## 文件清单

部署时需要上传以下文件：

```
index.html
app.js
styles.css
```

## 注意事项

- 无需服务器端环境（Node.js/Python 等）
- 无需数据库
- 数据存储在用户浏览器中，不涉及隐私数据传输
- 建议使用 HTTPS，确保 localStorage 正常工作
