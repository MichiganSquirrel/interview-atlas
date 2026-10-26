---
title: "一致性哈希"
title_en: "Consistent Hashing"
description: "一致性哈希"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["哈希键 / Hash key", "哈希环 / Ring", "后继节点 / Successor", "迁移区间 / Move range"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing"
---

# 一致性哈希

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![一致性哈希示意图](../../assets/07-consistent-hashing.svg)

## 核心判断

直接使用 `hash(key) % N`，节点数量变化会重映射大量键。一致性哈希（Consistent Hashing）把键与节点映射到同一哈希环（Hash Ring），常见实现选择顺时针的后继节点。

虚拟节点（Virtual Node）让单机占据多个环位置，改善分布并表达容量权重。理想均匀分布下，从 N 个节点增加一个节点大约迁移 `1/(N+1)` 的键；这不是任意工作负载下的严格保证。

## 面试推演：模型元数据缓存

节点加入后，只迁移它新接管的区间。缓存可以按新路由重建；持久化数据库还要处理数据搬迁、请求路由版本、迁移期间读写与副本恢复。

一致性哈希不保证副本数据一致，也不会自动解决单个超热键。热点需要拆分、复制读取或业务级限流。

## 自测

- [ ] 在纸上画三个节点的环，再加入第四个节点，标出迁移区间。
- [ ] 虚拟节点增加后，路由元数据和运维成本怎样变化？
- [ ] 节点宕机与主动扩容的处理有哪些不同？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Consistent Hashing](https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing)（核对日期：2026-10-25）。
