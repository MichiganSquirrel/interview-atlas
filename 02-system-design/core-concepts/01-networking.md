---
title: "网络基础"
title_en: "Networking Essentials"
description: "网络基础"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["客户端 / Client", "DNS + TLS", "负载均衡 / LB", "服务 / Service"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials"
---

# 网络基础

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![网络基础示意图](../../assets/01-networking.svg)

## 核心判断

域名系统（DNS）负责查址；TCP 提供有序、可靠的字节流；TLS 保护连接；HTTP 定义请求与响应。HTTP/3 基于 QUIC/UDP，不应把所有 HTTP 都说成 TCP。

负载均衡（Load Balancing）把流量分散到实例。四层（L4）依据连接信息，七层（L7）可依据 HTTP 路径或头部。长连接需要考虑连接数、保活与重连。

## 面试推演：训练任务进度

提交训练任务走 HTTP 请求；服务端单向推送进度可用服务器发送事件（SSE）；双向交互再考虑 WebSocket。先定义延迟和连接规模，再选协议。

| 追问 | 回答抓手 |
| --- | --- |
| 连接成功代表业务成功吗？ | TCP 成功不代表事务已提交，应用层要有确认和幂等。 |
| 为什么要超时？ | 限制等待时间，配合有限重试、退避（Backoff）和抖动（Jitter）。 |
| 网络调用真的很慢吗？ | 看跨区域距离、序列化、连接复用和尾延迟（Tail Latency）。 |

## 自测

- [ ] 画出浏览器到服务的路径，并说明每一层失败时用户看到什么。
- [ ] 解释 L7 路由与 L4 转发的差别。

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Networking Essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)（核对日期：2026-10-25）。
