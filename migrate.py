"""
数据迁移脚本：将 tasks.json 中的数据迁移到 SQLite 数据库
"""
import json
import requests
import sys

API_URL = "http://localhost:8000"


def load_json_data():
    """从 JSON 文件加载数据"""
    try:
        with open('tasks.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[错误] tasks.json 文件不存在")
        return []
    except json.JSONDecodeError:
        print("[错误] tasks.json 格式错误")
        return []


def migrate_to_database(tasks):
    """将任务迁移到数据库"""
    success_count = 0
    failed_count = 0

    for task in tasks:
        try:
            # 准备数据
            data = {
                "text": task.get("text", ""),
                "done": task.get("done", False),
                "priority": task.get("priority", "中")
            }

            # 调用 API 创建任务
            response = requests.post(f"{API_URL}/tasks", json=data, timeout=10)

            if response.status_code in (200, 201):
                success_count += 1
                print(f"[成功] 已迁移: {data['text'][:30]}...")
            else:
                failed_count += 1
                print(f"[失败] {data['text'][:30]}... (状态码: {response.status_code})")

        except requests.exceptions.Timeout:
            failed_count += 1
            print(f"[超时] {data['text'][:30]}...")
        except Exception as e:
            failed_count += 1
            print(f"[错误] {data['text'][:30]}... - {str(e)}")

    return success_count, failed_count


def main():
    print("=" * 50)
    print("待办事项数据迁移工具")
    print("=" * 50)
    print()

    # 检查后端服务
    try:
        response = requests.get(API_URL, timeout=5)
        print(f"[OK] 后端服务已连接: {API_URL}")
    except requests.exceptions.ConnectionError:
        print(f"[错误] 无法连接到后端服务: {API_URL}")
        print("请先启动后端服务: cd backend && uvicorn app.main:app --reload")
        sys.exit(1)

    print()

    # 加载 JSON 数据
    tasks = load_json_data()
    if not tasks:
        print("没有需要迁移的数据")
        return

    print(f"[信息] 发现 {len(tasks)} 个任务需要迁移")
    print()

    # 确认迁移
    confirm = input("确认开始迁移吗？ [Y/n]: ").strip().lower()
    if confirm and confirm not in ('y', 'yes'):
        print("已取消迁移")
        return

    print()
    print("开始迁移...")
    print("-" * 50)

    # 执行迁移
    success, failed = migrate_to_database(tasks)

    print("-" * 50)
    print()
    print("[完成] 迁移结束！")
    print(f"   成功: {success}")
    print(f"   失败: {failed}")
    print()
    print("现在你可以通过 http://localhost:8000 访问 API")
    print("通过打开 frontend/index.html 使用新界面")


if __name__ == "__main__":
    main()
