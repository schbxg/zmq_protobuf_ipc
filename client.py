"""
ZMQ + Protobuf IPC Client
使用 IPC 传输协议的客户端示例
"""
import zmq
import time
import uuid
from message_pb2 import Message, Request, Response, MessageType

# IPC 地址 (与服务器保持一致)
IPC_ADDRESS = "tcp://127.0.0.1:5555"


def create_request(method: str, params: str) -> Message:
    """创建请求消息"""
    request = Request()
    request.method = method
    request.params = params.encode('utf-8')
    
    msg = Message()
    msg.id = str(uuid.uuid4())
    msg.timestamp = int(time.time() * 1000)
    msg.sender = "client"
    msg.type = MessageType.REQUEST
    msg.payload = request.SerializeToString()
    
    return msg


def send_request(socket, method: str, params: str) -> Response:
    """发送请求并获取响应"""
    # 创建并发送请求
    request_msg = create_request(method, params)
    print(f"\n[Client] 发送请求: method={method}, params={params}")
    
    socket.send(request_msg.SerializeToString())
    
    # 接收响应
    response_data = socket.recv()
    
    # 解析响应消息
    response_msg = Message()
    response_msg.ParseFromString(response_data)
    
    # 解析响应内容
    response = Response()
    response.ParseFromString(response_msg.payload)
    
    return response


def main():
    """主函数"""
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(IPC_ADDRESS)
    
    print(f"[Client] 连接到服务器: {IPC_ADDRESS}")
    
    try:
        # 测试 echo 方法
        response = send_request(socket, "echo", "Hello, Protobuf + ZMQ!")
        print(f"[Client] Echo 响应: success={response.success}, result={response.result.decode('utf-8')}")
        
        # 测试 time 方法
        response = send_request(socket, "time", "")
        print(f"[Client] Time 响应: success={response.success}, result={response.result.decode('utf-8')}")
        
        # 测试 add 方法
        response = send_request(socket, "add", "10, 20, 30, 40")
        print(f"[Client] Add 响应: success={response.success}, result={response.result.decode('utf-8')}")
        
        # 测试未知方法
        response = send_request(socket, "unknown", "test")
        print(f"[Client] Unknown 响应: success={response.success}, error={response.error}")
        
    except KeyboardInterrupt:
        print("\n[Client] 客户端关闭")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
