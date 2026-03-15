"""
待办事项管理器 - 你的第一个 Python 桌面应用！
功能：添加任务、删除任务、标记完成
作者：你的名字
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# 数据文件路径（保存任务）
DATA_FILE = "tasks.json"

# 任务列表（程序运行时存储任务的地方）
tasks = []


def load_tasks():
    """从文件加载任务"""
    global tasks
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)


def save_tasks():
    """保存任务到文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task():
    """添加新任务"""
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        task_entry.delete(0, tk.END)
        refresh_task_list()
        save_tasks()
    else:
        messagebox.showwarning("提示", "请输入任务内容！")


def delete_task():
    """删除选中的任务"""
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        refresh_task_list()
        save_tasks()
    else:
        messagebox.showwarning("提示", "请先选中要删除的任务！")


def toggle_task():
    """标记任务完成/未完成"""
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks[index]["done"] = not tasks[index]["done"]
        refresh_task_list()
        save_tasks()
    else:
        messagebox.showwarning("提示", "请先选中要标记的任务！")


def refresh_task_list():
    """刷新任务列表显示"""
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✓ " if task["done"] else "○ "
        display_text = status + task["text"]
        task_listbox.insert(tk.END, display_text)
        # 完成的任务显示为灰色
        if task["done"]:
            task_listbox.itemconfig(tk.END, fg="gray")


# ============ 创建主窗口 ============
root = tk.Tk()
root.title("待办事项管理器")
root.geometry("500x400")
root.resizable(False, False)

# 设置窗口样式
style = ttk.Style()
style.configure("TButton", font=("微软雅黑", 10))

# ============ 顶部输入区域 ============
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill=tk.X)

task_entry = tk.Entry(frame_input, font=("微软雅黑", 12), width=35)
task_entry.pack(side=tk.LEFT, padx=(0, 10))
task_entry.bind('<Return>', lambda e: add_task())  # 按回车添加

btn_add = tk.Button(frame_input, text="添加任务", font=("微软雅黑", 10),
                    bg="#4CAF50", fg="white", width=10, command=add_task)
btn_add.pack(side=tk.LEFT)

# 搜索框
search_entry = tk.Entry(frame_input, font=("微软雅黑", 10), width=15, fg="gray")
search_entry.pack(side=tk.LEFT, padx=(20, 5))
search_entry.insert(0, "搜索任务...")

# 搜索框焦点事件
def on_search_focus_in(event):
    if search_entry.get() == "搜索任务...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")

def on_search_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, "搜索任务...")
        search_entry.config(fg="gray")
        refresh_task_list()  # 清空搜索时恢复全部任务

def search_tasks():
    """搜索任务功能"""
    keyword = search_entry.get().strip()
    if keyword == "搜索任务..." or keyword == "":
        refresh_task_list()
        return

    task_listbox.delete(0, tk.END)
    for task in tasks:
        if keyword.lower() in task["text"].lower():
            status = "✓ " if task["done"] else "○ "
            display_text = status + task["text"]
            task_listbox.insert(tk.END, display_text)
            if task["done"]:
                task_listbox.itemconfig(tk.END, fg="gray")

search_entry.bind('<FocusIn>', on_search_focus_in)
search_entry.bind('<FocusOut>', on_search_focus_out)
search_entry.bind('<KeyRelease>', lambda e: search_tasks())

# ============ 任务列表区域 ============
frame_list = tk.Frame(root, padx=10, pady=5)
frame_list.pack(fill=tk.BOTH, expand=True)

# 列表框 + 滚动条
scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox = tk.Listbox(frame_list, font=("微软雅黑", 11),
                          yscrollcommand=scrollbar.set,
                          selectmode=tk.SINGLE,
                          height=15,
                          activestyle='dotbox',  # 选中时的样式
                          selectbackground='#2196F3',  # 选中背景色（蓝色）
                          selectforeground='white')  # 选中文字颜色（白色）
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=task_listbox.yview)

# 双击任务也可以标记完成/未完成
task_listbox.bind('<Double-Button-1>', lambda e: toggle_task())
# 按 Delete 键删除任务
task_listbox.bind('<Delete>', lambda e: delete_task())

# 提示标签
hint_label = tk.Label(root, text="💡 单击选中任务，然后点击按钮 | 双击任务=标记完成 | 按 Delete 键=删除",
                      font=("微软雅黑", 9), fg="gray", pady=5)
hint_label.pack()

# ============ 按钮区域 ============
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill=tk.X)

btn_toggle = tk.Button(frame_buttons, text="✓ 标记完成/未完成", font=("微软雅黑", 10),
                       bg="#2196F3", fg="white", width=16, command=toggle_task)
btn_toggle.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(frame_buttons, text="🗑 删除任务", font=("微软雅黑", 10),
                       bg="#f44336", fg="white", width=12, command=delete_task)
btn_delete.pack(side=tk.LEFT, padx=5)

# ============ 启动程序 ============
load_tasks()  # 加载已有任务
refresh_task_list()

# 让输入框获得焦点
task_entry.focus()

# 运行主循环
root.mainloop()
