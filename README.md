# qqbot-tools
简称qt，基于[go-cqhttp框架](https://github.com/Mrs4s/go-cqhttp)开发的qq机器人
## 1.安装
### 1.1.下载并配置go-cqhttp框架

go-cqhttp帮助文档链接：[go-cqhttp](https://docs.go-cqhttp.org/)  
配置选择`HTTP通信`  
QQ号及密码及签名服务器自行配置   
http设置：  
```
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器

  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP监听地址
      version: 11     # OneBot协议版本, 支持 11/12
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      - url: http://127.0.0.1:5701/ # 地址
        secret: ''                  # 密钥
        max-retries: 10             # 最大重试，0 时禁用
        retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
```

### 1.2.安装qt
使用指令：  
> github源：`git clone git@github.com:EasonHelloWord/qqbot-tools.git`  
> gitee源：`git clone git@gitee.com:easonjan/qqbot-tools.git`  

或自行在线下载：  
>[github项目地址](https://github.com/EasonHelloWord/qqbot-tools)  
>[gitee项目地址](https://gitee.com/easonjan/qqbot-tools)  

运行main.py即可

## 2.用户功能：
| 类型 | 名称     | 描述                         |
| ---- | -------- | ---------------------------- |
| 主动 | 配置     | 配置文件                     |
| 主动 | 回声洞   | 在这里你可以听到任何人的声音 |
| 主动 | 帮助     | 帮助文档                     |
| 主动 | 一言     | 一句话服务，传递更多的感动   |
| 主动 | AI       | 让ai来和你聊天叭！           |
| 被动 | 闪照破解 | 用于破解闪照                 |
| 被动 | 撤回破解 | 用于破解撤回消息             |

### 配置

- **类型**: 主动功能
- **介绍**: 群聊中仅群主和管理员可配置此项，用于配置文件，每个会话独立
- **用法**:
  - 配置：输出所有已设置的配置
  - 配置[名称]:<内容>：将配置[名称]的值更新为<内容>（冒号不区分中英文符号）
  - 配置[名称]或配置[名称]:：删除[名称]的设置
- **示例**: 配置alarm_time:2023

### 回声洞

- **类型**: 主动功能
- **介绍**: 在这里你可以听到任何人的声音
- **用法**:
  - 回声：听一条回声
  - 回声洞[句子]：向回声洞说一句话
- **示例**: 回声洞今天天气不错

### 帮助

- **类型**: 主动功能
- **介绍**: 帮助文档
- **用法**:
  - 帮助：显示所有的功能和简介
  - 帮助[名称]：显示[名称]的详细介绍
- **示例**: 帮助回声洞

### 一言

- **类型**: 主动功能
- **介绍**: 一句话服务，传递更多的感动
- **用法**: 一言：收听一句话
- **示例**: 一言

### AI

- **类型**: 主动功能
- **介绍**: 让ai来和你聊天叭！性能原因回复较慢，上下文仅支持四轮，需由机器人拥有者配置后使用
- **用法**: ai[你想说的话]    和ai聊天
- **示例**: ai今天天气不错

### 闪照破解

- **类型**: 被动功能
- **介绍**: 用于破解闪照，默认为关
- **用法**: 配置ban_flash:[true/false]：启动或关闭闪照破解功能
- **示例**: 配置ban_flash:true

### 撤回破解

- **类型**: 被动功能
- **介绍**: 用于破解撤回消息，默认为关，仅对群聊有效，对机器人的消息永远无效
- **用法**: 配置ban_recall:[true/false]：启动或关闭闪照破解功能
- **示例**: 配置ban_recall:true

## 3.程序接口：
| 文件         | 方法                  | 描述           |
| ------------ | --------------------- | -------------- |
| cqhttp_tools | get_group_member_list | 获取群成员信息 |
| cqhttp_tools | get_admin_user_ids    | 获取管理员列表 |
| cqhttp_tools | get_group_member_info | 获取群成员信息 |
| cqhttp_tools | send_message          | 发送消息       |
| cqhttp_tools | get_msg               | 获取消息       |
| cqhttp_tools | get_login_info        | 获取登录号信息 |
| cqhttp_tools | post                  | 发送报文       |
| config       | get_config            | 读取配置文件   |
| config       | set_config            | 更新配置文件   |
| EchoCave     | EchoCave              | 写入回声洞     |
| EchoCave     | readfile              | 获取回声洞     |
| flash        | flash                 | 闪照破解       |
| group_recall | group_recall          | 撤回消息破解   |
| helps        | find_and_read_file    | 帮助文档细节   |
| helps        | read_all_file         | 所有的帮助文档 |
| repeat       | repeat                | 复读机         |
| yiyan        | yiyan                 | 读取一言       |
| ChatGLM      | ChatGLM               | ai聊天         |
