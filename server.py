"""
ZMQ + Protobuf IPC Server
使用 IPC 传输协议的服务端示例
"""
import zmq
import time
import uuid
from message_pb2 import Message, Request, Response, MessageType

# IPC 地址 (Windows 使用 tcp, Linux/Mac 可以使用 ipc://)
# Windows 不支持 ipc://, 使用 tcp://127.0.0.1 作为本地IPC替代
IPC_ADDRESS = "tcp://127.0.0.1:5555"

# Linux/Mac 可以使用:
# IPC_ADDRESS = "ipc:///tmp/zmq_protobuf.ipc"


def create_response(request_id: str, success: bool, result: bytes = b"", error: str = "") -> Message:
    """创建响应消息"""
    response = Response()
    response.success = success
    response.error = error
    response.result = result
    
    msg = Message()
    msg.id = str(uuid.uuid4())
    msg.timestamp = int(time.time() * 1000)
    msg.sender = "server"
    msg.type = MessageType.RESPONSE
    msg.payload = response.SerializeToString()
    
    return msg


def handle_request(request_data: bytes) -> Message:
    """处理请求"""
    # 解析消息
    msg = Message()
    msg.ParseFromString(request_data)
    
    print(f"[Server] 收到消息 ID: {msg.id}")
    print(f"[Server] 发送者: {msg.sender}")
    print(f"[Server] 时间戳: {msg.timestamp}")
    
    # 解析请求内容
    request = Request()
    request.ParseFromString(msg.payload)
    
    print(f"[Server] 方法: {request.method}")
    print(f"[Server] 参数: {request.params.decode('utf-8')}")
    
    # 处理不同的方法
    if request.method == "echo":
        return create_response(msg.id, True, request.params)
    elif request.method == "time":
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        return create_response(msg.id, True, current_time.encode('utf-8'))
    elif request.method == "add":
        try:
            params = request.params.decode('utf-8').split(',')
            result = sum(int(x.strip()) for x in params)
            return create_response(msg.id, True, str(result).encode('utf-8'))
        except Exception as e:
            return create_response(msg.id, False, error=str(e))
    else:
        return create_response(msg.id, False, error=f"Unknown method: {request.method}")


def main():
    """主函数"""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(IPC_ADDRESS)
    
    print(f"[Server] 服务器启动，监听地址: {IPC_ADDRESS}")
    print("[Server] 等待客户端连接...")
    
    try:
        while True:
            # 接收请求
            request_data = socket.recv()
            print("\n" + "="*50)
            
            # 处理请求
            response = handle_request(request_data)
            
            # 发送响应
            socket.send(response.SerializeToString())
            print(f"[Server] 响应已发送")
            
    except KeyboardInterrupt:
        print("\n[Server] 服务器关闭")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
