---
title: "网络基础"
title_en: "Networking Essentials"
description: "从 HTTPS 请求路径理解分层、TCP/UDP/QUIC、实时协议、负载均衡、区域化和故障恢复。"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["客户端 / Client", "DNS + TLS", "负载均衡 / LB", "服务 / Service"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials"





source_access: "authenticated-written-article-reviewed"
---

# 网络基础

网络设计决定请求经过哪些节点、各层提供什么保证，以及拥塞、断连和跨区域访问时服务如何退化。先把一条请求走通，再讨论协议、连接管理和负载分配，比直接堆组件更容易说明设计依据。

![网络请求的主要环节](../../assets/01-networking.svg)

## 一次 HTTPS 请求的完整路径

以浏览器查询训练任务为例：`GET /training-jobs/job-42`。客户端先通过域名系统（DNS）找到目标地址；没有可复用的连接时，再建立传输连接和 TLS 安全会话；随后发送 HTTP 请求。请求可能经过 CDN、负载均衡器、应用服务和数据库，响应沿相应连接返回。

这里有三种不同的时间：建立连接的时间、网络往返时间（Round-trip Time，RTT）和服务处理时间。即使数据库查询很快，跨洲 RTT、首次握手或代理排队仍可能占据主要延迟。连接复用（Connection Reuse）避免每次请求重新建立连接，因此不能把每次 HTTP 请求都画成一次全新的 TCP 握手。

DNS 记录有缓存和生存时间（TTL）。调整域名解析不意味着所有客户端立刻迁移，区域故障切换必须考虑旧地址缓存、已有连接与重新连接行为。TCP 连接在传输层建立成功，也不代表应用层任务已创建或事务已提交。

## 分层：IP、传输协议和应用协议各管什么

| 层次 | 负责的事情 | 不自动提供的保证 |
| --- | --- | --- |
| 网络层（L3）：IP | 地址与跨网络路由，尽力交付数据包。 | 不保证包一定到达，也不保证到达顺序。 |
| 传输层（L4）：TCP、UDP；QUIC 提供现代传输能力 | 端到端通信；具体保证由协议决定。 | 不保证业务操作只执行一次。 |
| 应用层（L7）：HTTP、DNS、WebSocket 等 | 定义请求、响应或消息的业务可理解格式。 | 不替应用设计鉴权、恢复或一致性规则。 |

端口（Port）区分同一主机上的通信端点。客户端连接的是某个地址与端口，不是抽象的“用户服务”；服务发现（Service Discovery）和负载均衡负责把逻辑服务映射到可用实例。

## TCP、UDP 与 QUIC

TCP 提供有序的可靠字节流，包含重传、流量控制（Flow Control）和拥塞控制（Congestion Control）。它不保留应用消息边界：一次写入的数据可能被拆成多次读取，应用需要长度前缀、分隔符或上层协议来分帧。发生丢包时，后续字节可能等待重传，影响尾延迟。

UDP 以数据报（Datagram）发送，不内建可靠交付、排序或拥塞控制。它适合由应用自己管理丢失和时效性的场景，例如实时媒体；过时的语音片段往往没有继续等待的价值。但“用了 UDP 就一定更快”不成立，补上的可靠性、拥塞控制与重传机制仍然有成本。

QUIC 建立在 UDP 之上，加入可靠流、加密和连接管理。HTTP/3 使用 QUIC；HTTP/1.1 和 HTTP/2 通常使用 TCP。QUIC 的独立流减少了某个流丢包对其他流的传输层队头阻塞（Head-of-line Blocking），但不等于消除了所有拥塞或等待。

## HTTP、TLS 与接口语义

HTTP 定义方法、状态码、头部和消息体。HTTP/1.1 可以复用连接；HTTP/2 可在一个连接中多路复用（Multiplexing）多个流。选择版本时应说明希望改善的瓶颈，而不是只把版本号当作性能结论。[MDN 的 HTTP 概览](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)说明了客户端、服务器与中间代理的关系。

HTTPS 在传输中提供机密性和完整性，并验证服务端身份。TLS 终止（TLS Termination）可以发生在边缘、负载均衡器或应用服务上；终止之后到后端的一段是否继续加密，是另外的部署选择。

加密不等于鉴权。请求体里写着 `owner_id=42`，不能证明发起者拥有该任务。服务端仍应验证身份、资源归属和操作权限。HTTP 的无状态语义也不意味着底层没有连接状态，或服务端不能使用会话。

## REST、GraphQL 与 gRPC 的位置

| 方式 | 适用场景 | 要说明的代价 |
| --- | --- | --- |
| REST | 面向资源的公开 Web 接口，例如查询和创建任务。 | 复杂页面可能需要聚合接口或多次请求。 |
| GraphQL | 不同客户端需要不同字段和关联数据。 | 解析器、查询复杂度、N+1 访问、缓存和权限控制更复杂。 |
| gRPC | 有稳定服务契约的内部调用，或流式服务通信。 | 浏览器端通常需要 gRPC-Web 或其他适配，运维链路也要支持。 |

gRPC 常用 Protocol Buffers 和 HTTP/2，并可以生成多语言客户端。二进制格式有利于减少部分序列化成本，但是否改善端到端延迟要看实际负载。REST、GraphQL 是接口设计方式，TCP、UDP 是传输方式，不能放在同一个层级直接替代比较。

## 实时更新：轮询、SSE 与 WebSocket

轮询（Polling）由客户端定期查询，实现简单，代价是重复请求和最多一个轮询间隔的额外等待。低频状态刷新可能已经足够，未必需要长连接。

服务器发送事件（Server-Sent Events，SSE）在 HTTP 响应流上从服务端向客户端推送文本事件，适合训练进度、通知和生成式输出。事件可以带 `id`；浏览器 `EventSource` 会尝试重新连接，并可用 `Last-Event-ID` 帮助服务器恢复游标。服务器是否保存事件、保存多久、如何补发，仍需应用实现，不能把自动重连当作不丢消息的保证。

SSE 还要处理代理缓冲、空闲超时和心跳；HTTP/1.1 环境下也要注意浏览器连接数限制。具体事件格式见 [MDN 的 SSE 文档](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)。

WebSocket 提供持久的双向消息通道。常见 HTTP/1.1 建连方式是先发起 HTTP Upgrade，再交换 WebSocket 帧；其他 HTTP 版本可以使用不同的建立机制。它适合频繁双向交互，例如协作操作和聊天。应用仍需定义消息类型、确认、顺序、心跳与恢复协议；一条 TCP 连接的可靠性不覆盖断线后的业务消息重放。

## WebRTC：媒体连接与 NAT 穿透

WebRTC 常用于浏览器音视频通信。信令（Signaling）交换双方的会话和连接候选信息；信令服务不必承载最终媒体流。ICE 负责收集和检查连接候选，STUN 帮助发现外部可达地址，无法直连时可以通过 TURN 中继。

所以“WebRTC 等于永远点对点、不需要服务器”是错误的。TURN 会带来中继带宽成本；多人会议常使用选择性转发单元（SFU）等服务器架构，避免每个参与者向所有其他人分别发送媒体流。[MDN 的连接说明](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity)可用于核对连接建立与候选交换机制。

## 负载均衡：分配请求还是分配连接

客户端负载均衡由客户端或其库发现实例并选择目标，省去一个集中转发点，但需要管理发现、健康状态和客户端版本。独立负载均衡器集中接收流量，便于统一策略，也要考虑其容量和故障切换。

| 选择 | 能依据什么分配 | 设计影响 |
| --- | --- | --- |
| L4 负载均衡 | IP、端口、连接等传输信息。 | 常按连接分配，不理解 HTTP 路径；具体实现可能透传或代理连接。 |
| L7 负载均衡 | HTTP 主机、路径、头部或 Cookie。 | 可做内容路由、TLS 终止和更细的应用策略，但需要应用协议处理。 |

L7 也可以支持 WebSocket；不能因为是长连接就机械地要求 L4。选择取决于是否需要检查 Upgrade 请求、按路径路由、执行应用策略，以及产品的实际支持能力。连接建立后通常固定到后端，新增实例不一定自动分担已有长连接。

轮询（Round Robin）、最少连接（Least Connections）、权重和一致性哈希解决的是不同负载模型。连接数量相同不代表 CPU 或请求量相同；健康检查通过也不保证实例没有过载。会话粘滞（Sticky Session）可以减少状态搬迁，却会增加倾斜与故障恢复难度。

## 跨区域与故障处理

CDN 缓存可复用内容，减少用户到源站的距离；它不能消除所有动态写请求的远程协调。区域化（Regionalization）把服务部署到用户附近，但必须另行决定数据归属、跨区复制、写入位置和故障接管。

超时（Timeout）约束一次调用的等待，截止时间（Deadline）约束整个操作的总预算。重试（Retry）要限次数、受总预算约束，并配合指数退避与随机抖动。多层各自重试会放大流量；存在副作用的调用还需要幂等键。熔断（Circuit Breaker）在下游持续失败时暂时停止调用，并通过有限探测判断恢复，避免故障扩散。[AWS 的重试设计文章](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)提供了这些机制的工程背景。

在训练平台里，可以把任务创建做成带幂等键的普通 HTTPS 请求，把进度展示做成可从事件游标恢复的 SSE，把高频交互单独放在 WebSocket 上。这样每种连接都有清晰职责，不需要用一种实时协议承载所有操作。

## 关联与学习入口

[API 设计](02-api-design.md) · [缓存](05-caching.md) · [容量估算](09-capacity-estimation.md) · [模块导航](../README.md)

已通过现有登录会话核对 [Hello Interview 的 Networking Essentials 书面章节](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)。本页按请求路径重新组织，并补充规范解释和训练平台例子；不转录课程视频或测验。
