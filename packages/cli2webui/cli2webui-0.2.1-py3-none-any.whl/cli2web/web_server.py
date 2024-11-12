# 确保在导入其他模块之前进行 monkey patch
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from .cli_parser import CliParser
from .web_generator import WebGenerator
from .process_manager import ProcessManager
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# 修改 Socket.IO 配置
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# 创建应用上下文
ctx = app.app_context()
ctx.push()

process_manager = ProcessManager(socketio)

# 存储命令名称的全局变量
command_name = None

def init_app(cmd_name):
    """初始化应用，设置命令名称"""
    global command_name
    command_name = cmd_name

@app.route('/')
def index():
    global command_name
    if not command_name:
        return "Error: No command specified", 500
        
    print(f"Processing command: {command_name}")
    
    parser = CliParser(command_name)
    options = parser.parse_help()
    print(f"Parsed options: {options}")
    
    options_dict = [opt.to_dict() for opt in options]
    
    generator = WebGenerator()
    form_html = generator.generate_form(command_name, options_dict)
    print(f"Generated HTML length: {len(form_html)}")
    
    return form_html

@app.route('/prepare', methods=['POST'])
def prepare():
    """准备执行命令，返回执行ID"""
    command_line = request.form.get('command_line', '').strip()
    if not command_line:
        return jsonify({
            'error': 'No command specified'
        }), 400
    
    execution_id = str(uuid.uuid4())
    print(f"Prepared execution ID: {execution_id}")
    
    return jsonify({
        'execution_id': execution_id
    })

@app.route('/execute', methods=['POST'])
def execute():
    """执行已准备好的命令"""
    command_line = request.form.get('command_line', '').strip()
    execution_id = request.form.get('execution_id', '').strip()
    
    if not command_line or not execution_id:
        return jsonify({
            'error': 'Missing command or execution ID'
        }), 400
    
    input_data = request.form.get('stdin', '')
    print(f"Starting execution: {execution_id} - {command_line}")
    
    # 启动命令执行
    process_manager.start_command(command_line, execution_id, input_data)
    
    return jsonify({
        'status': 'started'
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connect_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on_error_default
def default_error_handler(e):
    print(f'SocketIO error: {str(e)}')
    return False

def run_server(host='localhost', port=5000, cmd_name=None):
    """运行服务器"""
    try:
        if cmd_name:
            init_app(cmd_name)
        
        # 使用 eventlet 运行服务器
        socketio.run(
            app,
            host=host,
            port=port,
            debug=True,
            use_reloader=False,
            log_output=True
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        # 清理应用上下文
        ctx.pop()