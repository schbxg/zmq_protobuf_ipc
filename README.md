# ZMQ + Protobuf IPC 示例

使用 ZeroMQ 和 Protocol Buffers 进行进程间通信 (IPC) 的示例项目。

---

## Protocol Buffers 简介

### 什么是 Protocol Buffers？

**Protocol Buffers (Protobuf)** 是 Google 开发的一种语言无关、平台无关的高效序列化数据格式。它用于结构化数据的序列化，特别适用于网络通信和数据存储。

### 核心特点

| 特点 | 说明 |
|------|------|
| 🚀 **高效** | 二进制格式，比 JSON/XML 小 3-10 倍，解析速度快 20-100 倍 |
| 📝 **强类型** | 使用 `.proto` 文件定义数据结构，编译时类型检查 |
| 🌍 **跨语言** | 支持 C++, Java, Python, Go, C#, JavaScript 等主流语言 |
| 🔄 **版本兼容** | 支持向前/向后兼容，便于 API 演进 |
| 📦 **代码生成** | 自动生成序列化/反序列化代码 |

### 与 JSON/XML 对比

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   特性       │  Protobuf   │    JSON     │    XML      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ 格式         │ 二进制       │ 文本         │ 文本        │
│ 大小         │ 最小         │ 中等         │ 最大        │
│ 解析速度     │ 最快         │ 中等         │ 最慢        │
│ 可读性       │ 不可读       │ 可读         │ 可读        │
│ Schema      │ 必须         │ 可选         │ 可选        │
│ 类型安全     │ 强           │ 弱           │ 弱          │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 基本使用流程

```
1. 定义消息 (.proto)     →  message Person { string name = 1; int32 age = 2; }
2. 编译生成代码          →  protoc --python_out=. person.proto
3. 使用生成的类          →  person = Person(); person.name = "Alice"
4. 序列化/反序列化       →  data = person.SerializeToString()
```

### 适用场景

- ✅ 微服务间通信 (gRPC)
- ✅ 进程间通信 (IPC)
- ✅ 嵌入式设备/IoT (资源受限环境)
- ✅ 大规模数据存储
- ✅ 高性能 RPC 系统

### 不适用场景

- ❌ 需要人工阅读/编辑数据
- ❌ 浏览器直接使用 (推荐 JSON)
- ❌ 简单的配置文件

---

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
