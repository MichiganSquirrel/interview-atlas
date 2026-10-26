---
title: "Core Concepts 全章导航"
title_en: "Core Concepts: Complete Topic Index"
description: "Core Concepts 全章导航"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
---

# Core Concepts 全章导航

这里是九篇可连续阅读的主题讲解。所有正文直接平铺，不需要点击展开，也不包含自测或测验。每章解释概念、工作机制、适用场景和代价，并用具体例子连接设计决策。

| 章节 | 正文内容 |
| --- | --- |
| [网络基础](01-networking.md) | 请求路径、分层与协议、实时通信、负载均衡、区域化与故障恢复。 |
| [API 设计](02-api-design.md) | 资源契约、异步操作、幂等、分页、授权与兼容演进。 |
| [数据建模](03-data-modeling.md) | 访问模式、实体关系、约束、并发状态、对象存储与生命周期。 |
| [数据库索引](04-database-indexing.md) | 数据页、B-tree 与 LSM、复合和覆盖索引、执行计划与维护成本。 |
| [缓存策略与失效](05-caching.md) | 缓存位置、读写模式、新鲜度、失效竞态、热点与故障回源。 |
| [数据分片](06-sharding.md) | 分片键、放置规则、热点、跨分片操作和在线迁移。 |
| [一致性哈希](07-consistent-hashing.md) | 取模重映射、哈希环、虚拟节点、成员版本与复制边界。 |
| [CAP 与一致性取舍](08-cap-theorem.md) | 分区下的读写行为、不同一致性模型和端到端读取语义。 |
| [容量估算与数量级](09-capacity-estimation.md) | 请求与数据量、带宽、并发、资源限制、队列与故障余量。 |

## 阅读顺序

网络与 API → 数据模型与索引 → 缓存 → 分片与一致性哈希 → CAP → 容量估算。这个顺序先讲一条请求如何执行，再讨论如何扩展和处理故障；也可以直接按左侧链接进入需要的主题。

## 图示与离线阅读

每章正文内附有可直接预览的 SVG。[系统设计交互总览](../../assets/system-design-map.html)可下载为独立 HTML；完整阅读包包含全部中英文正文、图示和 Obsidian 笔记。

## 阅读依据

已通过现有登录会话核对 Hello Interview 的九个书面主题。本站按系统问题重新组织讲解，并引用相关规范、官方文档与独立算例；没有转录课程视频或测验。其他 Patterns、Key Technologies 和设计题不属于本组九篇的范围。

[Hello Interview 课程目录](https://www.hellointerview.com/learn/courses/system-design) · [返回系统设计模块](../README.md)
