# ZMQ + Protobuf IPC 示例

使用 ZeroMQ 和 Protocol Buffers 进行进程间通信 (IPC) 的示例项目。

## 项目结构

```
zmq_protobuf_ipc/
├── message.proto      # Protobuf 消息定义
├── message_pb2.py     # 生成的 Python 代码 (需要编译生成)
├── server.py          # IPC 服务端
├── client.py          # IPC 客户端
├── requirements.txt   # Python 依赖
└── README.md          # 说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 编译 Protobuf

首先需要安装 protoc 编译器，然后编译 .proto 文件：

### Windows (使用 pip 安装的 grpcio-tools)

```bash
pip install grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. message.proto
```

### 或者使用 protoc 编译器

```bash
protoc --python_out=. message.proto
```

## 运行示例

### 1. 启动服务端

```bash
python server.py
```

### 2. 运行客户端 (新终端)

```bash
python client.py
```

## 消息格式

### Message (通用消息)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 消息唯一ID |
| timestamp | int64 | 时间戳 (毫秒) |
| sender | string | 发送者标识 |
| payload | bytes | 实际数据 |
| type | MessageType | 消息类型 |

### 支持的方法

- `echo`: 回显传入的参数
- `time`: 返回服务器当前时间
- `add`: 计算参数中数字的和 (用逗号分隔)

## IPC 地址说明

- **Windows**: 使用 `tcp://127.0.0.1:5555` (Windows 不支持 Unix domain socket)
- **Linux/Mac**: 可以使用 `ipc:///tmp/zmq_protobuf.ipc`

## 扩展

可以根据需要修改 `message.proto` 添加更多消息类型，然后重新编译生成 Python 代码。
