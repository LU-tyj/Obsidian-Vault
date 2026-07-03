---
title: "HTTP与HTTPS"
category: 计算机基础
tags: [计算机网络, HTTP, 网易互娱]
frequency: ⭐
difficulty: 简单
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[TCP vs UDP与可靠传输]]"
  - "[[TCP三次握手四次挥手]]"
---

## 🎯 一句话结论（自测用）
> HTTP 是明文传输的请求-响应协议（基于 TCP），HTTPS = HTTP + TLS/SSL 加密，通过非对称加密交换会话密钥、对称加密传输数据、证书体系验证身份。HTTP/1.1 的 Keep-Alive 允许单 TCP 连接发送多个请求（连接复用），减少 TCP 握手开销。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **HTTP 与 TCP 的连接关系**：
   - HTTP 基于 TCP，但 HTTP 请求/响应是"消息"层面，TCP 是"传输"层面
   - HTTP/1.0：每次请求新建一次 TCP 连接（短连接），用完就关
   - HTTP/1.1（Keep-Alive）：单 TCP 连接可以复用，连续发送多个请求（长连接）
   - HTTP/2：单 TCP 连接上的多路复用（Stream），多个请求并发而不互相阻塞

2. **HTTPS 的工作原理**：
   - 在 HTTP 和 TCP 之间加入 TLS/SSL 层
   - **握手阶段**：非对称加密（RSA/ECDHE）交换会话密钥
   - **数据传输**：对称加密（AES）加密实际数据（非对称太慢）
   - **身份验证**：数字证书 + CA 链验证服务器身份
   - **完整性校验**：HMAC 防止数据被篡改

3. **HTTP vs HTTPS**：

| 维度 | HTTP | HTTPS |
|------|------|-------|
| 端口 | 80 | 443 |
| 加密 | 明文传输 | TLS 加密 |
| 身份验证 | 无 | 数字证书 |
| SEO | 搜索引擎降权 | 搜索引擎偏好 |
| 性能 | 快（无加密开销） | 略慢（首次握手开销大） |

## 🔍 详细解析

**TLS 握手简略流程**：
1. Client Hello：客户端发送支持的加密套件 + 随机数
2. Server Hello：服务器选加密套件 + 证书 + 随机数
3. 客户端验证证书，生成 Pre-Master Secret，用服务器公钥加密发送
4. 双方从三个随机数推导出会话密钥
5. 后续用对称加密传输

**游戏中的 HTTP 使用**：
- 登录/认证（HTTP/HTTPS API）
- 资源下载（HTTP 下载 AssetBundle）
- 玩家数据上报、排行榜查询
- 实时通信仍用 TCP/UDP Socket，不走 HTTP

## 💬 面试官常见追问
- "HTTP 的长连接和短连接？" -> 短连接：一次请求/响应就关闭 TCP。长连接（Keep-Alive）：TCP 连接保持，多个请求复用。WebSocket 也是一种长连接（全双工）
- "HTTP/2 相比 HTTP/1.1 的改进？" -> 多路复用（解决队头阻塞）、头部压缩（HPACK）、服务器推送、二进制分帧

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：HTTPS 所有数据都慢。首次握手慢（非对称加密 + 证书验证），建立会话后对称加密几乎不影响吞吐量
- 误区：HTTP 就是 TCP。HTTP 是应用层协议，TCP 是传输层协议，两个不同层次

## 🔗 关联知识点
- [[TCP vs UDP与可靠传输]]
- [[TCP三次握手四次挥手]]

## 📎 原始出处
- 牛客网006 Q21: HTTP与TCP连接复用关系（HTTP/1.1的keep-alive）
