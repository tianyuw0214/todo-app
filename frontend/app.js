// API 基础 URL，可从外部配置覆盖
// 生产环境使用相对路径，开发环境使用 localhost
const API_URL = (typeof window !== 'undefined' && window.API_CONFIG?.baseUrl)
    || (window.location.hostname === 'localhost'
        ? 'http://localhost:8000'
        : '');  // 生产环境使用相对路径，自动匹配当前域名
let allTasks = [];
let currentFilter = 'all'; // all, active, completed

// 获取所有任务
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        allTasks = await response.json();
        renderTasks();
        updateStats();
    } catch (error) {
        console.error('加载任务失败:', error);
        showError('无法连接到服务器，请确保后端服务已启动');
    }
}

// 渲染任务列表
function renderTasks() {
    const taskList = document.getElementById('taskList');

    // 根据筛选条件过滤任务
    let tasksToShow = allTasks;
    if (currentFilter === 'active') {
        tasksToShow = allTasks.filter(t => !t.done);
    } else if (currentFilter === 'completed') {
        tasksToShow = allTasks.filter(t => t.done);
    }

    // 按创建时间倒序
    tasksToShow.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    if (tasksToShow.length === 0) {
        const emptyText = {
            'all': { title: 'No Articles Yet', sub: 'Start by creating your first task' },
            'active': { title: 'All Caught Up', sub: 'No drafts pending publication' },
            'completed': { title: 'No Published Works', sub: 'Complete some tasks to see them here' }
        }[currentFilter];
        taskList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-text">${emptyText.title}</div>
                <div class="empty-state-sub">${emptyText.sub}</div>
            </div>
        `;
        return;
    }

    taskList.innerHTML = tasksToShow.map((task, index) => `
        <div class="task-item ${task.done ? 'task-done' : ''}" data-id="${task.id}" style="animation-delay: ${index * 0.05}s">
            <div class="checkbox ${task.done ? 'checked' : ''}" data-action="toggle">
                ${task.done ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>` : ''}
            </div>
            <span class="task-text">${escapeHtml(task.text)}</span>
            <div class="task-meta">
                <span class="priority-tag priority-${getPriorityClass(task.priority)}">${getPriorityLabel(task.priority)}</span>
                <div class="delete-btn" data-action="delete">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                </div>
            </div>
        </div>
    `).join('');
}

// 更新统计信息
function updateStats() {
    const total = allTasks.length;
    const completed = allTasks.filter(t => t.done).length;
    const active = total - completed;

    animateNumber('statTotal', total);
    animateNumber('statActive', active);
    animateNumber('statCompleted', completed);
}

// 数字动画
function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    const currentValue = parseInt(element.textContent, 10);
    if (currentValue === targetValue) return;

    const duration = 400;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const value = Math.round(currentValue + (targetValue - currentValue) * easeProgress);
        element.textContent = value;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// 设置筛选条件
function setFilter(filter) {
    currentFilter = filter;

    // 更新按钮状态
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`filter-${filter}`).classList.add('active');

    renderTasks();
}

// 处理 API 错误响应
async function handleApiError(response, defaultMessage) {
    if (response.status === 422) {
        const error = await response.json();
        const detail = error.detail;
        if (Array.isArray(detail) && detail.length > 0) {
            showError(`输入验证失败: ${detail[0].msg || '请检查输入'}`);
        } else {
            showError('输入验证失败，请检查输入内容');
        }
    } else if (response.status === 404) {
        showError('任务不存在');
    } else {
        showError(`${defaultMessage} (${response.status})`);
    }
}

// 添加任务
async function addTask() {
    const input = document.getElementById('taskInput');
    const prioritySelect = document.getElementById('prioritySelect');
    const text = input.value.trim();

    if (!text) {
        showError('请输入任务内容');
        return;
    }

    if (text.length > 500) {
        showError('任务内容不能超过 500 字符');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                done: false,
                priority: prioritySelect.value
            })
        });

        if (response.status === 201) {
            input.value = '';
            document.getElementById('charCount').textContent = '0/500';
            loadTasks();
        } else {
            await handleApiError(response, '添加任务失败');
        }
    } catch (error) {
        console.error('添加任务失败:', error);
        showError('添加任务失败，请检查网络连接');
    }
}

// 切换任务状态
async function toggleTask(id, done) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ done: done })
        });

        if (response.ok) {
            loadTasks();
        } else {
            await handleApiError(response, '更新任务失败');
        }
    } catch (error) {
        console.error('更新任务失败:', error);
        showError('更新任务失败，请检查网络连接');
    }
}

// 删除任务
async function deleteTask(id) {
    if (!confirm('确定要删除这个任务吗？')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });

        if (response.status === 204 || response.ok) {
            loadTasks();
        } else {
            await handleApiError(response, '删除任务失败');
        }
    } catch (error) {
        console.error('删除任务失败:', error);
        showError('删除任务失败，请检查网络连接');
    }
}

// 获取优先级样式类
function getPriorityClass(priority) {
    const map = {
        '高': 'high',
        '中': 'medium',
        '低': 'low'
    };
    return map[priority] || 'medium';
}

// 获取优先级英文标签
function getPriorityLabel(priority) {
    const map = {
        '高': 'Urgent',
        '中': 'Normal',
        '低': 'Low'
    };
    return map[priority] || priority;
}

// 转义 HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 显示错误信息
function showError(message) {
    const toast = document.getElementById('errorToast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// 页面加载时获取任务
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();

    // 绑定回车键添加任务
    document.getElementById('taskInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // 使用事件委托处理任务列表点击
    document.getElementById('taskList').addEventListener('click', function(e) {
        const taskItem = e.target.closest('.task-item');
        if (!taskItem) return;

        const taskId = parseInt(taskItem.dataset.id, 10);
        if (!taskId) return;

        const actionEl = e.target.closest('[data-action]');
        if (!actionEl) return;

        const action = actionEl.dataset.action;

        if (action === 'toggle') {
            const isDone = !taskItem.classList.contains('task-done');
            toggleTask(taskId, isDone);
        } else if (action === 'delete') {
            deleteTask(taskId);
        }
    });
});
