## 1 Reference
[一文搞懂什么是socket编程](https://cloud.ofweek.com/news/2019-06/ART-178803-11000-30394087.html#:~:text=简称套接字，是,服务端，一个客户端%E3%80%82)
[CSDN](https://blog.csdn.net/qq_42824983/article/details/117913721)

---

## 2 Introduce
Socket（套接字）是计算机网络通信的基石，它是应用层与TCP/IP协议栈通信的中间软件抽象层，负责在不同主机或同一主机的**不同进程间建立双向连接并传输数据**。

它工作在传输层（通常是TCP/UDP），提供了 `socket()`、`bind()`、`listen()`、`connect()`、`send()`、`recv()` 等 API，允许通过IP和端口进行数据交换。

### 2.1 核心概念与工作原理
- **物理映射**：Socket 被形象地称为网络“插座”或“插口”，是数据传输的通道。
- **组成要素**：一个Socket通信由“IP地址+端口号+协议”组成，决定了数据发送的目的地和方式。
- **通信模式**：基于C/S（客户端-服务器）架构。服务端先初始化Socket并监听，客户端发起连接，连接建立后进行双向数据读写。
- **文件描述符**：在Unix/Linux中，Socket被视为一种特殊文件，操作遵循“打开-读写-关闭”模式。 

### 2.2 关键组件
- **TCP Socket**：提供面向连接的、可靠的、基于字节流的通信（如 `SOCK_STREAM`）。
- **UDP Socket**：提供无连接的、不可靠的、基于数据报的通信（如 `SOCK_DGRAM`）。
- **[Socket.IO](https://www.google.com/search?client=safari&rls=en&q=Socket.IO&ie=UTF-8&oe=UTF-8&mstk=AUtExfDl1J3Qj7OfdEAH764DR99lK804WxbTJfDDXxLYBM5wPxdCoW212g2Bw1EvAaye5M33_XtEH-JEmZYdBvBFZcmkzlSlqvDlUvAX38xGNg7TR_dihLFnn0AV5hd8XZy9TNUO3CwRVtOX7_FDL_I5MQ8HcnCyf_p5RoZMnBfau1BMJWU&csui=3&ved=2ahUKEwjLhPrb6IKTAxXErlYBHTFYCdIQgK4QegQIBRAD)**：一个基于事件的、在客户端和服务器之间提供实时、双向通信的库，通常用于Web应用

### 2.3 Socket编程基本流程
1. **Server**: `socket()` -> `bind()` -> `listen()` -> `accept()` -> `read/write` -> `close()`
2. **Client**: `socket()` -> `connect()` -> `write/read` -> `close()`

---

## 3 Specific Code
>windows 中需要调用 `WSAStartup` 来初始化网络库和 `WSACleanup` 来进行清理。
>而mac和linux上不用。所以写跨平台要用宏定义 `#ifdef _WIN32` 和 `#endif`
>这两个函数为**进程级**函数，即可以在任意线程都可以调用，如果一个线程调用了 `WSACleanup` 其他都没法用。

### 3.1 socket方法
创建服务器套接字
```cpp
SOCKET server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

if (server_socket == INVALID_SOCKET)
{
	std::cerr << "Socket creation failed: " << WSAGetLastError() << std::endl;
	WSACleanup();
	return 1;
}
```

`int socket (int domain, int type, int protocol)`
- **domain**: 使用的协议族，这里 `AF_INET` 指的是 IPV4
- **type**: 创建网络连接类型。TCP可以用`SOCK_STREAM`（数据包有序、可靠），UDP可以用`SOCK_DRAM` （数据包代表离散的报文）
- **protocol**: socket 发送数据时使用的协议，包括传输层协议以及各种实用网络层协议，主要使用的是`IPPROTO_TCP`和`IPPROTO_UDP`（就如其名）

### 3.2 使用 close 关闭 socket 释放资源
```cpp
#ifdef _WIN32
closesocket(server_socket);
#endif

close(server_socket)
```
>因为win自己有个 `close()` 所以必须用 `closesocket()`

### 3.3 bind -- TCP的下一步
为创建好的 socket 绑定本地IP和端口号。使用`sockaddr_in`结构体，其属性有：协议族、IP、端口号
```cpp
// 设置服务器地址信息
sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_addr.s_addr = INADDR_ANY; // 监听所有网络接口
server_addr.sin_port = htons(8888); // 监听端口8888

// 绑定套接字到本地地址
if (bind(server_socket, (sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR)
{
	std::cerr << "Bind failed: " << WSAGetLastError() << std::endl;
	closesocket(server_socket);
	WSACleanup();
	return 1;
}
```

`int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);`
- **sockfd**: 创建的socket
- **addr**: 上文所说的结构体
- **addrlen**: 地址长度

### 3.4 listen 进入监听状态
```cpp
// 开始监听连接请求
if (listen(server_socket, SOMAXCONN) == SOCKET_ERROR)
{
	std::cerr << "Listen failed: " << WSAGetLastError() << std::endl;
	closesocket(server_socket);
	WSACleanup();
	return 1;
}

std::cout << "Server listening on port 8888..." << std::endl;
```

`int listen(int sockfd, int backlog);`
- **sockfd**: socket
- **backlog**: 相应socket可以排队的最大连接数

### 3.5 accept
在监听的对中选择一个连接请求，并且创建一个新的socket
```cpp
// 接受客户端连接
sockaddr_in client_addr;
int client_addr_size = sizeof(client_addr);

SOCKET client_socket = accept(server_socket, (sockaddr*)&client_addr, &client_addr_size);

if (client_socket == INVALID_SOCKET)
{
	std::cerr << "Accept failed: " << WSAGetLastError() << std::endl;
	closesocket(server_socket);
	WSACleanup();
	return 1;
}

std::cout << "Client connected!" << std::endl;
```
>原本的socket只负责连接，通过`accept`创建的新socket才负责数据通信

### 3.6 connect 客户端连接
`connect(client_socket, (sockaddr*)&server_addr, sizeof(server_addr))`

这样可以建立客户端和服务器之间的连接

### 3.7 send/recv 
在已建立的连接上进行数据的发送接收（默认情况下是阻塞式的）
```cpp
// 通信循环
char recv_buf[1024];
int bytes_received;
while (true)
{
	// 接收客户端数据
	bytes_received = recv(client_socket, recv_buf, sizeof(recv_buf), 0);
	if (bytes_received > 0)
	{
		std::cout << "Received: " << recv_buf << std::endl;
		
		// 发送响应消息
		const char* response = "Message received by server";
		send(client_socket, response, (int)strlen(response) + 1, 0);
	}
	else if (bytes_received == 0)
		{
		std::cout << "Client disconnected." << std::endl;
		break;
	}
	else
	{
		std::cerr << "recv failed: " << WSAGetLastError() << std::endl;
		break;
	}
}
```

```cpp
// TCP 数据传输接收函数
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);

// UDP 数据传输接收函数
ssize_t sendto(int sockfd, const void *buf, size_t len, int flags, 
				const struct sockaddr *dest_addr, socklen_t addrlen);
ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags, 
				struct sockaddr *src_addr, socklen_t *addrlen);
```

### 3.8 Pipeline
这是最简单的连接方式。
![[Socket流程图.png]]

当我们需要处理多个连接时，为了防止阻塞阻止游戏内循环，有两种方式：
- 阻塞 IO 配合多线程：给每个可能的阻塞调用生成一个线程，优点是方便直观，缺点是资源占用大
- 非阻塞 IO 配合单线程
