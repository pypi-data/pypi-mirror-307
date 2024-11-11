import subprocess
import threading
import uuid
from typing import Optional, Dict
from queue import Queue
import shlex
import time
import io
import sys
import select

class ProcessManager:
    def __init__(self, socketio):
        self.socketio = socketio
        self.processes: Dict[str, subprocess.Popen] = {}
        self.output_queues: Dict[str, Queue] = {}
        
    def start_command(self, command: str, execution_id: str, input_data: Optional[str] = None) -> None:
        """使用指定的执行ID启动命令"""
        print(f"[DEBUG] Starting command execution with ID: {execution_id}")
        
        def run_command():
            try:
                command_args = shlex.split(command)
                print(f"[DEBUG] Executing command with args: {command_args}")
                
                process = subprocess.Popen(
                    command_args,
                    stdin=subprocess.PIPE if input_data else None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    bufsize=1
                )
                
                self.processes[execution_id] = process
                print(f"[DEBUG] Process created with PID: {process.pid}")
                
                def read_output(pipe, pipe_name):
                    """读取输出流"""
                    try:
                        print(f"[DEBUG] Starting {pipe_name} reader for execution {execution_id}")
                        buffer = []
                        
                        # 使用 select 监控输出流
                        while True:
                            ready, _, _ = select.select([pipe], [], [], 0.1)
                            if ready:
                                line = pipe.readline()
                                if not line and process.poll() is not None:
                                    break
                                if line:
                                    print(f"[DEBUG] Read from {pipe_name}: {line.rstrip()}")
                                    buffer.append(line)
                                    self.socketio.emit('command_output', {
                                        'execution_id': execution_id,
                                        'output': line,
                                        'pipe': pipe_name
                                    })
                                    print(f"[DEBUG] Emitted {pipe_name} output for {execution_id}")
                                    # 确保消息被发送
                                    self.socketio.sleep(0)
                            elif process.poll() is not None:
                                # 进程已结束，检查是否还有剩余输出
                                remaining = pipe.read()
                                if remaining:
                                    print(f"[DEBUG] Read remaining {pipe_name}: {remaining.rstrip()}")
                                    buffer.append(remaining)
                                    self.socketio.emit('command_output', {
                                        'execution_id': execution_id,
                                        'output': remaining,
                                        'pipe': pipe_name
                                    })
                                    print(f"[DEBUG] Emitted remaining {pipe_name} output for {execution_id}")
                                    self.socketio.sleep(0)
                                break
                        
                        print(f"[DEBUG] Total {pipe_name} lines read: {len(buffer)}")
                        return buffer
                        
                    except Exception as e:
                        print(f"[ERROR] Error reading from {pipe_name}: {e}", file=sys.stderr)
                        return []
                
                # 创建输出处理线程
                print(f"[DEBUG] Creating output threads for {execution_id}")
                stdout_thread = threading.Thread(
                    target=lambda: read_output(process.stdout, 'stdout'),
                    name=f"stdout-{execution_id}"
                )
                stderr_thread = threading.Thread(
                    target=lambda: read_output(process.stderr, 'stderr'),
                    name=f"stderr-{execution_id}"
                )
                
                # 启动线程
                stdout_thread.start()
                stderr_thread.start()
                print(f"[DEBUG] Output threads started for {execution_id}")
                
                # 如果有输入数据，写入stdin
                if input_data:
                    try:
                        print(f"[DEBUG] Writing input data for {execution_id}")
                        process.stdin.write(input_data)
                        process.stdin.flush()
                        process.stdin.close()
                        print(f"[DEBUG] Input data written for {execution_id}")
                    except Exception as e:
                        print(f"[ERROR] Error writing to stdin: {e}", file=sys.stderr)
                
                # 等待进程完成
                print(f"[DEBUG] Waiting for process {execution_id} to complete")
                return_code = process.wait()
                print(f"[DEBUG] Process {execution_id} completed with return code: {return_code}")
                
                # 等待输出线程完成
                stdout_thread.join()
                stderr_thread.join()
                print(f"[DEBUG] Output threads completed for {execution_id}")
                
                # 发送命令完成事件
                print(f"[DEBUG] Sending command complete event for {execution_id}")
                self.socketio.emit('command_complete', {
                    'execution_id': execution_id,
                    'return_code': return_code
                })
                # 确保完成事件被发送
                self.socketio.sleep(0)
                print(f"[DEBUG] Command complete event sent for {execution_id}")
                
            except Exception as e:
                print(f"[ERROR] Error executing command: {e}", file=sys.stderr)
                self.socketio.emit('command_error', {
                    'execution_id': execution_id,
                    'error': str(e)
                })
                self.socketio.sleep(0)
            finally:
                # 清理进程
                if execution_id in self.processes:
                    try:
                        print(f"[DEBUG] Cleaning up process {execution_id}")
                        self.processes[execution_id].kill()
                    except:
                        pass
                    del self.processes[execution_id]
                    print(f"[DEBUG] Process {execution_id} cleaned up")
        
        # 在新线程中启动命令
        thread = threading.Thread(target=run_command, name=f"command-{execution_id}")
        thread.daemon = True
        thread.start()
        print(f"[DEBUG] Command thread started for {execution_id}")