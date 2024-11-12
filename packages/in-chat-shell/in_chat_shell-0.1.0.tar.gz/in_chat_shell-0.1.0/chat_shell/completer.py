from prompt_toolkit.completion import PathCompleter, WordCompleter, merge_completers
from prompt_toolkit.completion import Completer, Completion
import os
from prompt_toolkit.document import Document

# 自定义命令补全器

class CommandCompleter(Completer):
    def __init__(self):
        # 基础命令字典
        self.commands = {
            'ls': 'List directory contents',
            'cd': 'Change directory',
            'pwd': 'Print working directory',
            'vim': 'Text editor',
            'cat': 'Concatenate and print files',
            'grep': 'File pattern searcher',
            'git': 'Version control system',
            'docker': 'Container management',
            'chat': 'Chat with llm',
            'history': 'Show command history',
            'exit': 'Exit the shell',
            'clear': 'Clear screen',
            'help': 'Show help message',
        }
        
        # 从PATH中获取所有可执行命令
        self.system_commands = self._get_system_commands()
        
        # 初始化路径补全器
        self.path_completer = PathCompleter(
            only_directories=False,
            expanduser=True,
            get_paths=lambda: ['.']
        )

    def _get_system_commands(self):
        """获取系统PATH中的所有可执行命令"""
        commands = {}
        paths = os.environ.get('PATH', '').split(os.pathsep)
        
        for path in paths:
            if os.path.exists(path):
                for cmd in os.listdir(path):
                    cmd_path = os.path.join(path, cmd)
                    if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                        commands[cmd] = f'System command: {cmd_path}'
        
        return commands

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        if not text:
            return self._get_command_completions('')

        try:
            words = text.split()
            if not words:
                return self._get_command_completions('')

            if len(words) == 1 and not text.endswith(' '):
                return self._get_command_completions(words[0])

            if len(words) > 1 or text.endswith(' '):
                last_word = words[-1] if not text.endswith(' ') else ''
                path_document = Document(last_word, len(last_word))
                return self.path_completer.get_completions(path_document, complete_event)

        except Exception as e:
            print(f"Completion error: {e}")
            return []

    def _get_command_completions(self, word):
        """生成命令补全建议，包括内置命令和系统命令"""
        # 合并内置命令和系统命令
        all_commands = {**self.commands, **self.system_commands}
        
        for cmd, desc in all_commands.items():
            if cmd.startswith(word):
                yield Completion(
                    cmd,
                    start_position=-len(word),
                    display_meta=desc
                )