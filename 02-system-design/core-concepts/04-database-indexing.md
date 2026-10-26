---
title: "数据库索引"
title_en: "Database Indexing"
description: "数据库索引"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["访问模式 / Query", "索引 / Index", "执行计划 / Plan", "测量 / Measure"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing"
---

# 数据库索引

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![数据库索引示意图](../../assets/04-database-indexing.svg)

## 核心判断

索引（Index）减少定位记录时读取的数据页。B-tree 适合等值、范围和排序；哈希索引（Hash Index）侧重等值；倒排索引（Inverted Index）适合词项检索；空间索引（Spatial Index）支持位置查询。LSM 结构以写入、合并与读取成本作权衡。

索引会消耗空间并增加写入维护开销。复合索引（Composite Index）的列序要匹配过滤与排序；覆盖索引（Covering Index）是否避免访问表数据还取决于数据库的可见性等条件。

## 面试推演：读取某实验最近的任务

```sql
CREATE INDEX jobs_experiment_recent
ON jobs (experiment_id, created_at DESC, id DESC);

SELECT id, state, created_at FROM jobs
WHERE experiment_id = 42
ORDER BY created_at DESC, id DESC LIMIT 20;
```

这个索引优先定位实验，再沿时间顺序读取。改成仅按 `state` 查询，效果可能不同。用执行计划（EXPLAIN）验证扫描行数、排序和实际耗时；低选择性（Selectivity）查询未必适合索引。

## 自测

- [ ] 为什么不能给每一列都加索引？
- [ ] `(a,b)` 为什么不等同于 `(b,a)`？
- [ ] 写入吞吐、读取延迟、空间放大之间怎么取舍？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Database Indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing)（核对日期：2026-10-25）。
