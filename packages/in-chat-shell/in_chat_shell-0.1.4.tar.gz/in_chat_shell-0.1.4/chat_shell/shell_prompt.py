import os 
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory

from chat_shell.completer import CommandCompleter
from pygments.lexers.shell import BashLexer
from prompt_toolkit.formatted_text import HTML

class ShellPrompt:
    def __init__(self):
        # 创建风格
        self.style = Style.from_dict({
            'username': '#00ff00 bold',  # 绿色用户名
            'at': '#ffffff',             # 白色@
            'host': '#00ff00 bold',      # 绿色主机名
            'path': '#0000ff bold',      # 蓝色路径
            'prompt': '#ff0000',         # 红色提示符
            'shell-output': '#ffffff',   # 白色输出
            'error': '#ff0000 bold',     # 红色错误
        })

        # 创建历史记录
        history_file = os.path.expanduser('~/.smart_shell_history')
        self.session = PromptSession(
            history=FileHistory(history_file),
            lexer=PygmentsLexer(BashLexer),
            # completer=SmartCompleter(),  # 使用新的补全器
            completer = CommandCompleter(),
            style=self.style,
            complete_while_typing=True,
            complete_in_thread=True,  # 在线程中进行补全，避免阻塞

            # 添加以下配置
            enable_history_search=True,
            auto_suggest=None,  # 禁用自动建议
            # accept_default=False,  # 禁用自动接受默认值
            # complete_style=CompleteStyle.COLUMN,  # 使用列形式显示补全
            # 禁用 Tab 键自动执行
            key_bindings=None,
        )

    def get_prompt_text(self):
        """生成提示符文本，支持conda环境显示"""
        username = os.getenv('USER', 'user')
        hostname = os.uname().nodename
        cwd = os.getcwd()
        home = os.path.expanduser('~')
        if cwd.startswith(home):
            cwd = '~' + cwd[len(home):]

        # 检查conda环境
        conda_env = os.getenv('CONDA_DEFAULT_ENV')
        
        if conda_env:
            # 如果存在conda环境，添加到提示符中
            return HTML(
                '(<conda>{}</conda>) '  # conda环境名
                '<username>{}</username>'
                '<at>@</at>'
                '<host>{}</host>'
                '<path>:{}</path>'
                '<prompt>$ </prompt>'
            ).format(conda_env, username, hostname, cwd)
        else:
            # 如果不存在conda环境，使用原来的格式
            return HTML(
                '<username>{}</username>'
                '<at>@</at>'
                '<host>{}</host>'
                '<path>:{}</path>'
                '<prompt>$ </prompt>'
            ).format(username, hostname, cwd)

    async def get_input(self):
        """获取用户输入"""
        try:
            return await self.session.prompt_async(
                self.get_prompt_text(),
                wrap_lines=False,
            )
        except KeyboardInterrupt:
            return None
