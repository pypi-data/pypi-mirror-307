from chat_shell.chat_session import ChatSession
from chat_shell.shell_prompt import ShellPrompt

import os
import termios
import sys
import tty
import pty
import select
import subprocess
import signal

class SmartShell:
    def __init__(self):
        self.chat_session = ChatSession()
        self.prompt = ShellPrompt()
        self.setup_terminal()
        self.debug_mode = False  # 可以通过命令开启/关闭调试模式

        # 设置信号处理
        signal.signal(signal.SIGINT, self.handle_sigint)
        self.current_process = None

    def handle_sigint(self, signum, frame):
        """处理 Ctrl+C 信号"""
        if self.current_process:
            try:
                self.current_process.terminate()
            except:
                pass
        else:
            # 如果没有正在运行的进程，打印新行并继续
            print('\n', end='', flush=True)

    def setup_terminal(self):
        """设置终端颜色和样式"""
        # 确保终端支持颜色
        os.environ['TERM'] = os.environ.get('TERM', 'xterm-256color')

    def print_colored(self, text, color='white', style=''):
        """打印彩色文本"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
        }
        styles = {
            'bold': '\033[1m',
            'underline': '\033[4m',
        }
        reset = '\033[0m'
        
        color_code = colors.get(color, '')
        style_code = styles.get(style, '')
        print(f"{color_code}{style_code}{text}{reset}")
    def run_interactive_command(self, command: str):
        """运行交互式命令"""
        # 保存当前终端设置
        old_attrs = termios.tcgetattr(sys.stdin)
        try:
            # 设置终端为raw模式
            tty.setraw(sys.stdin)
            
            # 创建子进程运行命令
            pid, fd = pty.fork()
            
            if pid == 0:  # 子进程
                # 执行命令
                os.execvp(command.split()[0], command.split())
            else:  # 父进程
                self.current_process = pid  # 保存当前进程 ID
                try:
                    while True:
                        try:
                            r, w, e = select.select([sys.stdin, fd], [], [])
                            
                            if sys.stdin in r:
                                data = os.read(sys.stdin.fileno(), 1024)
                                os.write(fd, data)
                            
                            if fd in r:
                                data = os.read(fd, 1024)
                                if not data:
                                    break
                                os.write(sys.stdout.fileno(), data)
                        except (IOError, OSError):
                            break
                except KeyboardInterrupt:
                    # 处理 Ctrl+C
                    os.kill(pid, signal.SIGINT)
                finally:
                    self.current_process = None
                    
        finally:
            # 恢复终端设置
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attrs)
        
    def is_interactive_command(self, command: str) -> bool:
        """判断是否是交互式命令"""
        interactive_commands = ['vim', 'nano', 'less', 'more', 'top', 'htop', 'vi', 'emacs']
        command_name = command.strip().split()[0]
        return command_name in interactive_commands
    def capture_command_output(self, command: str, print_output: bool = True) -> tuple[str, int]:
        """执行shell命令并实现流式输出"""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.current_process = process  # 保存当前进程引用
            output = []
            
            # 使用非阻塞方式读取输出
            import fcntl
            import os
            
            # 设置非阻塞模式
            fcntl.fcntl(process.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(process.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
            
            while True:
                stdout_line = stderr_line = ''
                
                try:
                    stdout_line = process.stdout.readline()
                except IOError:
                    pass
                    
                try:
                    stderr_line = process.stderr.readline()
                except IOError:
                    pass
                    
                if stdout_line:
                    if print_output:
                        print(stdout_line, end='', flush=True)
                    output.append(stdout_line)
                if stderr_line:
                    if print_output:
                        self.print_colored(stderr_line, color='red')
                    output.append(stderr_line)
                    
                if not stdout_line and not stderr_line:
                    # 检查进程是否结束
                    if process.poll() is not None:
                        # 确保读取所有剩余输出
                        remaining_stdout, remaining_stderr = process.communicate()
                        if remaining_stdout:
                            if print_output:
                                print(remaining_stdout, end='', flush=True)
                            output.append(remaining_stdout)
                        if remaining_stderr:
                            if print_output:
                                self.print_colored(remaining_stderr, color='red')
                            output.append(remaining_stderr)
                        break
                        
            return ''.join(output), process.returncode
        except KeyboardInterrupt:
            # 处理 Ctrl+C
            if process:
                process.terminate()
                process.wait()
            return "Command interrupted by user", 130    
        except Exception as e:
            return str(e), 1
        finally:
            self.current_process = None  # 清除进程引用

    def handle_builtin_command(self, command: str) -> tuple[str, int]:
        """处理内置命令"""
        cmd_parts = command.strip().split()
        cmd = cmd_parts[0]
        
        if cmd == 'cd':
            try:
                # 处理空参数的情况，默认切换到用户主目录
                if len(cmd_parts) == 1:
                    target = os.path.expanduser('~')
                else:
                    target = os.path.expanduser(cmd_parts[1])
                
                os.chdir(target)
                return '', 0  # 成功时返回空输出和0返回码
            except FileNotFoundError:
                return f"cd: {cmd_parts[1]}: No such file or directory", 1
            except PermissionError:
                return f"cd: {cmd_parts[1]}: Permission denied", 1
            except Exception as e:
                return f"cd: {str(e)}", 1
        
        # 如果不是内置命令，返回 None 表示需要正常执行外部命令
        return None
    def handle_pipeline(self, command: str) -> tuple[str, int]:
        """处理管道命令"""
        commands = command.split('|')
        if len(commands) <= 1:
            return None  # 不是管道命令
            
        prev_output = None
        return_code = 0
        
        # 用于调试的处理日志
        pipeline_log = []
        
        for i, cmd in enumerate(commands):
            cmd = cmd.strip()
            is_last_command = (i == len(commands) - 1)  # 是否是最后一个命令
            stage_log = {"stage": i+1, "command": cmd, "type": "command"}
            
            if cmd.startswith('chat '):
                try:
                    if cmd[5:].strip().startswith('"'):
                        chat_prompt = cmd[5:].strip().strip('"')
                    elif cmd[5:].strip().startswith("'"):
                        chat_prompt = cmd[5:].strip().strip("'")
                    else:
                        chat_prompt = cmd[5:].strip()
                except Exception:
                    return "Error: Invalid chat prompt format", 1

                is_first_chat = (i == 0)
                result = self.chat_session.pipeline_chat(
                    chat_prompt, 
                    prev_output, 
                    is_first_chat=is_first_chat
                )
                prev_output = result
                
                stage_log["type"] = "chat"
                stage_log["is_first_chat"] = is_first_chat

            else:
                # 处理普通shell命令
                if prev_output is None:
                    # 第一个命令
                    output, rc = self.capture_command_output(cmd, print_output=is_last_command)
                else:
                    # 将前一个命令的输出通过管道传递给下一个命令
                    try:
                        process = subprocess.Popen(
                            cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        output, error = process.communicate(input=prev_output)
                        rc = process.returncode
                        if error:
                            output = output + error
                        # 只有在最后一个命令时才打印输出
                        # if is_last_command:
                        #     print(output, end='')
                    except Exception as e:
                        return str(e), 1
                
                prev_output = output
                return_code = rc if rc != 0 else return_code

            stage_log["output"] = prev_output
            stage_log["return_code"] = return_code
            pipeline_log.append(stage_log)

            # 显示调试信息
            if self.debug_mode:
                self.print_stage_debug_info(stage_log)

        # 将完整的管道命令及其最终输出添加到全局上下文
        self.chat_session.add_pipeline_context(command, prev_output, return_code)
                
        return prev_output, return_code

    def print_stage_debug_info(self, stage_log: dict):
        """打印每个阶段的调试信息"""
        stage_num = stage_log["stage"]
        cmd = stage_log["command"]
        cmd_type = stage_log["type"]
        
        if cmd_type == "chat":
            type_desc = "chat (with history)" if stage_log["is_first_chat"] else "chat (pipeline context)"
        else:
            type_desc = "shell command"
            
        self.print_colored(f"\nStage {stage_num}: {type_desc}", color='cyan')
        self.print_colored(f"Command: {cmd}", color='yellow')
        self.print_colored("Output:", color='yellow')
        print(stage_log["output"])
        if stage_log["return_code"] != 0:
            self.print_colored(f"Return code: {stage_log['return_code']}", color='red')
            

    async def run(self):
        self.print_colored("Welcome to Smart Shell!", color='green', style='bold')
        self.print_colored("Pipeline commands and their outputs are now saved in conversation history", color='cyan')
        self.print_colored("Use 'toggle_debug' to see detailed pipeline processing", color='cyan')
        self.print_colored("Use 'history' to view conversation history", color='cyan')
        self.print_colored("Use 'exit' to quit", color='yellow')
        self.print_colored("Use 'help' for more information", color='cyan')

        while True:
            output = ''
            try:
                # 获取用户输入
                user_input = await self.prompt.get_input()
                if user_input is None :
                    continue
                if  user_input.lower() == 'exit':
                    break
                
                # 空内容处理
                if not user_input.strip():
                    continue

                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                if user_input.lower() == 'toggle_debug':
                    self.debug_mode = not self.debug_mode
                    self.print_colored(
                        f"Debug mode {'enabled' if self.debug_mode else 'disabled'}", 
                        color='yellow'
                    )
                    continue
                    
                if user_input.lower() == 'history':
                    self.chat_session.debug_history()
                    continue

                return_code = 0
                # 处理命令
                pipeline_result = self.handle_pipeline(user_input)
                if pipeline_result is not None:
                    output, return_code = pipeline_result
                    if return_code != 0:
                        self.print_colored(output, color='red')
                    else:
                        print(output)
                else:
                    if user_input.lower().startswith('chat '):
                        chat_content = user_input[5:]
                        output = self.chat_session.chat(chat_content)
                        print(output)
                    else:
                        # 首先检查是否是内置命令
                        builtin_result = self.handle_builtin_command(user_input)
                        
                        if builtin_result is not None:
                            # 如果是内置命令，使用其返回结果
                            output, return_code = builtin_result
                            if return_code != 0:
                                self.print_colored(output, color='red')
                            else:
                                print(output, end='')
                        elif self.is_interactive_command(user_input):
                            self.print_colored("\nEntering interactive mode...", color='yellow')
                            self.run_interactive_command(user_input)
                            output, return_code = '', 0
                            if return_code != 0:
                                self.print_colored(output, color='red')
                            else:
                                print(output, end='')
                        else:
                            output, return_code = self.capture_command_output(user_input)
                        
                        
                
                # 添加对话历史
                self.chat_session.add_shell_context(user_input, output, 
                                                    return_code)
                self.chat_session.trim_conversation_history()
            except KeyboardInterrupt:
                # 处理主循环中的 Ctrl+C
                print('\n', end='', flush=True)
                continue
            except Exception as e:
                self.print_colored(f"Error: {str(e)}", color='red', style='bold')

    def show_help(self):
        """显示帮助信息"""
        help_text = """
        Smart Shell Commands:
        --------------------
        chat <message>  : Chat with llm
        help           : Show this help message
        history        : Show conversation history
        clear          : Clear the screen
        exit           : Exit the shell

        Special Features:
        ---------------
        - Tab completion for commands
        - Command history (up/down arrows)
        - Syntax highlighting
        - Interactive command support (vim, nano, etc.)
        - Context-aware AI assistance
        """
        self.print_colored(help_text, color='cyan')