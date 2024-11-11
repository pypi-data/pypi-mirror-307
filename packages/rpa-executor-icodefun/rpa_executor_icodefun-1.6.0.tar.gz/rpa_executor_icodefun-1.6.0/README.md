# 智码坊-RPA执行器（rpa-executor-icodefun）

这是智码坊的RPA执行器，配合智码坊可以完成以下工作：
- 自动注册受执行器管理的基于Robot Framework的RPA任务
- 通过智码坊后台任务调度中心
  - 管理并查看RPA执行器
  - 管理并查看RPA任务
  - 手动触发RPA任务的执行
  - 查看RPA历史执行情况
- 可通过Sailing或智码坊的开发平台发起RPA任务，并查询RPA任务执行结果


## 安装

### 安装python

智码坊-RPA执行器（以下简称rpa执行器）是一个python项目，因此首先需要安装python以及相关环境。rpa执行器支持`3.11.0`以上的版本。

### 创建虚拟环境

首先在任意位置建立目录，并在命令行中进入该目录。然后执行以下命令：

```shell
python -m venv .venv
```

以上命令将在目录中创建`.venv`目录，该目录存放了python虚拟环境信息，由工具自动维护，不要手动更改里面的任何东西。

然后执行以下命令激活虚拟环境。

在Windows上，运行：

```shell
.venv/Scripts/activate.bat
``` 

在linux上，运行：

```shell
source .venv/bin/activate
```

激活虚拟环境将改变你所用终端的提示符，以显示你正在使用的虚拟环境，并修改环境以使 python 命令所运行的将是已安装的特定 Python 版本。

需了解更多venv的用法，请看：https://docs.python.org/zh-cn/3.11/tutorial/venv.html


### 在虚拟环境中安装执行器

确保虚拟环境激活的情况，在命令行中执行以下命令：
```shell
pip install rpa-executor-icodefun
```

等安装完成后，再运行：

```shell
rfbrowser init
```

这个命令将下载浏览器RPA操作相关的一系列库，将近800MB，请耐心等待。

如果需要更新RPA执行器，运行：

```shell
pip install --upgrade rpa-executor-icodefun
```

## 配置执行器

RPA执行器采用约定加配置的风格定义运行时行为，首先需要一个配置文件，在目录中新建一个名为`config.yaml`，内容以及说明如下：

```yaml
xxl_admin_baseurl: "http://192.168.0.1:9970/xxl-job-admin/api/" # 智码坊后台调度中心的API url。注意修改ip和port

client_id: "rpa1" # 智码坊后台调度中心的用户名
client_secret: "123456" # 智码坊后台调度中心的密码

executor:
  app_name: "rpa-executor-1" # 本RPA执行器的名称。如果有多个rpa执行器需要注册到同一个调度中心，那么他们的名称最好有所区别，否则将导致任务重复执行。
  host: "192.168.64.16" # 报告本调度器的执行器IP。
  port: 9999 # 报告本调度器的执行器端口。
  # listen_host: None # 仅在执行器需经过代理访问时用到。https://fcfangcc.github.io/pyxxl/apis/config/#pyxxl.ExecutorConfig.executor_host
  # listen_port: 9999 # 仅在执行器需经过代理访问时用到。


log:
  log_dir: "logs" # 主日志所在目录。每次任务都会产生独立的日志
  expired_days: 7 # 主日志过期时间，单位：天

max_workers: 10 # 最大并发执行数。

task:
  queue_length: 10 # 最大等待队列长度
  timeout: 600 # 任务超时时间
```

## 配置任务

在目录中新建一个名为`tasks`的目录，每组RPA任务Suite单独建立一个目录，每个子目录中都要有一个`manifest.yaml`文件，以及RPA任务文件。下面是RPA执行器完整目录的例子：

```
rpa1
├ tasks
│ ├ task1
│ │ ├ manifest.yaml
│ │ ├ xxx.robot
│ │ └ ...
│ └ task1
│   ├ manifest.yaml
│   ├ xxx.robot
│   └ ...
└ config.yaml
```

`manifest.yaml`文件内容如下：

```yaml
name: "suite name" # 任务suite名称，仅可能和任务文件夹的名称保持一致，以方便管理
robot_file: "xxx.robot" # 任务suite的.robot文件名
description: "" # 任务suite描述
tasks: 
  -
    name: "task name 1" # xxx.robot 中的任务名称
    description: "task name 1" # 任务描述
  -
    name: "task name 2" # xxx.robot 中的另一个任务名称
    description: "task name 2" # 另一个任务描述
  - 
    ...
```


## 启动执行器

确保虚拟环境激活的情况，在执行器目录中执行 以下命令：

```shell
irpa dev
```

RPA执行器代码库的sample目录是一个实际的案例

http://git.tradeserving.com/icodefun/rpa-executor-icodefun/-/tree/master/sample?ref_type=heads

## 开发RPA任务

### 环境搭建

RPA任务基于robot framework以及rpa framework。robot framework有一套自己的脚本语言，脚本语言很简单，配合vscode插件编写十分方便，配套的rcc工具用于调试RPA任务。以下是开发环境搭建说明：https://docs.robotframework.org/docs/getting_started/rpa


### 开发

RPA执行器源码库中`sample/tasks/demo/tasks.robot`是一个实际的示例，可以通过这个项目来了解一个典型的RPA任务是怎么样的。


### 参考

开发过程中会用到的库说明：
- robot内置库：https://robotframework.org/?tab=builtin#resources
  - Builtin：https://robotframework.org/robotframework/latest/libraries/BuiltIn.html
  - Collections：https://robotframework.org/robotframework/latest/libraries/Collections.html
  - DateTime：https://robotframework.org/robotframework/latest/libraries/DateTime.html
  - Dialogs：https://robotframework.org/robotframework/latest/libraries/Dialogs.html
  - OperatingSystem：https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
  - Process：https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
  - Remote：https://robotframework.org/robotframework/latest/libraries/Process.html
  - Screenshot：https://robotframework.org/robotframework/latest/libraries/Screenshot.html
  - String：https://robotframework.org/robotframework/latest/libraries/String.html
  - Telnet：https://robotframework.org/robotframework/latest/libraries/Telnet.html
  - XML：https://robotframework.org/robotframework/latest/libraries/XML.html
- rpa framework库
  - https://rpaframework.org/index.html



