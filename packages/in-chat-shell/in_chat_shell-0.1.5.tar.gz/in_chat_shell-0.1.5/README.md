## smart_shell

基于python库`prompt_toolkit` 实现的一款命令行终端， 再保持现有shell功能的背景下，额外支持以下功能

1. 终端支持chat命令， 可以在命令行和大模型聊天
2. 终端支持chat读取命令行上下文， 支持读取历史shell命令的输入、输出结果
3. 在pipeline管道中, 支持chat命令读取管道命令的输出，输出

### 安装

```shell

pip intall in-chat-shell

```

### 进入shell

```
in-chat-shell
```


### 功能点1

在命令行中输入`chat`命令，进入聊天模式，可以和大模型聊天

```shell
> chat 你是什么模型
```


### 功能点2

在命令行中输入`chat`命令，进入聊天模式，可以和大模型聊天

```shell
chat 刚才git执行，为啥报错
```

### 功能点3

在pipline管道中， 支持chat命令读取管道命令的输出，输出

```shell

> ls -ls |  chat 转换为markdown格式

```