---
title: "缓存策略与失效"
title_en: "Caching & Invalidation"
description: "缓存策略与失效"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["请求 / Request", "缓存 / Cache", "未命中 / Miss", "数据库 / Database"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/caching"
---

# 缓存策略与失效

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![缓存策略与失效示意图](../../assets/05-caching.svg)

## 核心判断

缓存（Cache）用空间和一致性复杂度换取读延迟与后端负载改善。可放在客户端、CDN、应用进程或共享缓存层。旁路缓存（Cache-aside）先读缓存，未命中再读数据库并回填。

生存时间（TTL）限制驻留时间，但不自动保证业务允许的最大陈旧度。淘汰（Eviction）与过期（Expiration）不同。写穿（Write-through）、写回（Write-back）和失效策略具有不同持久性风险。

## 面试推演：任务状态读取

训练任务终态很少变化，适合缓存；活跃状态应依据进度新鲜度要求设置刷新策略。键加入尝试编号或版本，避免旧工作进程回填过期值。

| 故障 | 处理方向 |
| --- | --- |
| 热点同时过期（Stampede） | 单次回源（Single-flight）、过期时间抖动。 |
| 不存在的键持续穿透 | 短时负缓存（Negative Caching），必要时加布隆过滤器。 |
| 缓存整体不可用 | 限流、降级与回源并发上限，保护数据库。 |

## 自测

- [ ] 数据库更新成功，但缓存删除失败怎么办？
- [ ] 读到旧值后回填，能否覆盖刚写入的新值？
- [ ] 命中率很高时，为什么 p99 仍可能很差？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Caching & Invalidation](https://www.hellointerview.com/learn/system-design/core-concepts/caching)（核对日期：2026-10-25）。
