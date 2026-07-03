---
title: "I-O复用 select poll epoll"
category: 计算机基础
tags: [计算机网络, I/O, 网易互娱]
frequency: ⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[TCP vs UDP与可靠传输]]"
  - "[[进程vs线程]]"
---

## 🎯 一句话结论（自测用）
> select、poll、epoll 都是 I/O 多路复用机制，允许单线程同时监听多个 Socket。select 用固定大小位图（1024 上限）、poll 用动态数组（无上限但 O(n) 遍历）、epoll 用内核事件驱动 + 红黑树（仅返回就绪 fd，O(1) 获取，大数据量下性能碾压 select/poll）。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）

**三大 I/O 复用机制对比**：

| 维度 | select | poll | epoll |
|------|--------|------|-------|
| **数据结构** | 固定大小位图(fd_set) | 动态数组(pollfd) | 红黑树+就绪链表 |
| **最大连接数** | 1024(默认) | 无上限 | 无上限 |
| **fd 拷贝** | 每次调用复制整个 fd_set 到内核 | 每次调用复制整个数组 | 一次 epoll_ctl 注册，后续不拷贝 |
| **就绪检测** | O(n) 遍历所有 fd | O(n) 遍历所有 fd | O(1) 回调 + 只遍历就绪 fd |
| **工作模式** | 水平触发(LT) | 水平触发(LT) | LT + ET(边缘触发) |
| **适用场景** | 少量连接 | 少量连接 | **大量连接** |

**epoll 的核心优势**：
- 事件驱动：fd 就绪时内核通过回调将其加入就绪链表，`epoll_wait` 直接取
- 内存映射(mmap)：减少内核态到用户态的数据拷贝
- 支持 ET（边缘触发）：fd 状态变化时才通知（适合高性能场景，需配合非阻塞 I/O）

## 🔍 详细解析

**水平触发(LT) vs 边缘触发(ET)**：
- **LT（默认）**：只要 fd 就绪且有数据，每次 epoll_wait 都通知。编程简单，不易丢事件
- **ET**：fd 从不可读变为可读时才通知一次。必须用非阻塞 I/O 循环读取直到 EAGAIN，否则可能漏事件。性能更高但编程复杂

**Reactor vs Proactor**（与 I/O 复用相关）：
- **Reactor**：同步非阻塞 I/O + I/O 复用（epoll），I/O 和业务在同一线程。主循环通过 epoll 等事件，就绪后自行 read/write。代表：libevent、Netty(NIO)、Redis
- **Proactor**：异步 I/O，内核完成 I/O 后通知应用程序。代表：Windows IOCP、Boost.Asio（模拟）

**游戏服务器中的使用**：
- 游戏服务器通常用 epoll 管理大量客户端连接
- 结合线程池处理业务逻辑（Reactor 模式）
- 帧同步服务器简单（转发），状态同步服务器计算量大

## 💬 面试官常见追问
- "为什么 select 有 1024 的限制？" -> fd_set 用位图实现，默认大小 FD_SETSIZE = 1024。可以修改宏重编译，但不推荐——超过 1024 时 select 的 O(n) 遍历效率已经很差
- "epoll 的 ET 模式需要注意什么？" -> 必须用非阻塞 I/O + 循环读写直到返回 EAGAIN，否则漏事件后不会再次通知

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：epoll 一定比 select 快。在连接数很少（< 几十个）时，select 的简单实现可能比 epoll 的系统调用开销更小
- 误区：epoll 是异步 I/O。epoll 是 I/O 复用（同步非阻塞），I/O 操作本身还是同步的。真正的异步 I/O 是 Windows IOCP 那种——内核完成 I/O 后通知应用

## 🔗 关联知识点
- [[TCP vs UDP与可靠传输]]
- [[进程vs线程]]

## 📎 原始出处
- 牛客网014 Q10: I/O复用（select/poll/epoll）
