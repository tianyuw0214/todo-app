"""
启动脚本 - 一键启动待办事项 Web 应用
"""
import subprocess
import sys
import time
import os
import signal
import urllib.request
import urllib.error


def wait_for_service(url, max_retries=15, retry_interval=1):
    """等待服务启动，轮询检查"""
    for i in range(max_retries):
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except urllib.error.URLError:
            time.sleep(retry_interval)
        except Exception:
            time.sleep(retry_interval)
    return False


def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        stdout=None,  # 让输出直接显示在终端
        stderr=None,
    )

    # 等待服务启动
    print("等待服务启动...")
    if wait_for_service("http://localhost:8000"):
        print("后端服务已启动: http://localhost:8000")
        print("API 文档: http://localhost:8000/docs")
        return backend_process
    else:
        # 启动失败
        backend_process.terminate()
        print("错误: 后端服务启动失败，请检查依赖是否安装")
        print("运行: pip install -r backend/requirements.txt")
        sys.exit(1)


def main():
    print("=" * 50)
    print("待办事项 Web 应用启动器")
    print("=" * 50)
    print()

    backend_process = None

    try:
        # 启动后端
        backend_process = start_backend()
        print()

        # 显示访问信息
        print("应用已就绪！")
        print()
        print("请打开浏览器访问: frontend/index.html")
        print()
        print("或者使用以下地址:")
        print("  - 前端页面: file:///" + os.path.abspath("frontend/index.html").replace("\\", "/"))
        print("  - 后端 API: http://localhost:8000")
        print("  - API 文档: http://localhost:8000/docs")
        print()
        print("按 Ctrl+C 停止服务")
        print()

        # 保持运行
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("正在停止服务...")

    finally:
        if backend_process:
            backend_process.terminate()
            print("后端服务已停止")


if __name__ == "__main__":
    main()
