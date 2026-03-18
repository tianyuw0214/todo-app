import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建应用
app = Flask(__name__, static_folder='../frontend')

# 数据库配置
database_url = os.getenv('DATABASE_URL', 'sqlite:///todos.db')
# 修复 Render PostgreSQL URL 格式
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS
CORS(app)

# 数据库模型
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='中')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'done': self.done,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# 创建表
with app.app_context():
    try:
        db.create_all()
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库创建失败: {e}")

# API 路由
@app.route('/api/')
def api_root():
    return jsonify({'message': '待办事项 API 运行中', 'version': '2.0'})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    search = request.args.get('search', '')
    query = Task.query
    if search:
        query = query.filter(Task.text.contains(search))
    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': '任务内容不能为空'}), 422
    if len(text) > 500:
        return jsonify({'error': '任务内容不能超过500字符'}), 422

    task = Task(
        text=text,
        done=data.get('done', False),
        priority=data.get('priority', '中')
    )
    db.session.add(task)
    db.session.commit()
    logger.info(f"创建任务: {text[:50]}...")

    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404

    data = request.get_json()

    if 'text' in data:
        text = data['text'].strip()
        if not text:
            return jsonify({'error': '任务内容不能为空'}), 422
        task.text = text
    if 'done' in data:
        task.done = data['done']
    if 'priority' in data:
        task.priority = data['priority']

    task.updated_at = datetime.utcnow()
    db.session.commit()
    logger.info(f"更新任务 {task_id}")

    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404

    db.session.delete(task)
    db.session.commit()
    logger.info(f"删除任务 {task_id}")

    return '', 204

# 前端路由
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # 如果是 API 路径，返回 404
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404

    # 尝试返回静态文件
    try:
        return send_from_directory('../frontend', path)
    except:
        # 如果文件不存在，返回 index.html（支持前端路由）
        return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
