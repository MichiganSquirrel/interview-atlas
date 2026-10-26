---
title: "数据建模"
title_en: "Data Modeling"
description: "数据建模"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["查询 / Queries", "实体 / Entities", "约束 / Constraints", "存储 / Storage"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling"
---

# 数据建模

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![数据建模示意图](../../assets/03-data-modeling.svg)

## 核心判断

从查询与不变量（Invariant）反推实体、主键（Primary Key）、关系和约束。关系型数据库（Relational Database）是常见起点；选文档、键值或图模型时，需要说明具体访问模式。

规范化（Normalization）减少重复与更新异常；反规范化（Denormalization）用重复数据换取读取效率，同时引入更新与修复成本。事务的 ACID 不能替代对隔离级别（Isolation Level）的说明。

## 面试推演：实验、任务与检查点

```sql
experiments(id PRIMARY KEY, owner_id, config_version)
jobs(id PRIMARY KEY, experiment_id, state, attempt)
checkpoints(id PRIMARY KEY, job_id, object_key, step)
```

模型权重放对象存储（Object Storage），表里保存位置、版本与校验信息。任务尝试编号区分重试；状态转换采用条件更新，防止旧工作进程覆盖新尝试。检查点是否可用，以完整写入和元数据提交为界。

## 自测

- [ ] 如何查询某个实验最新的成功检查点？该建什么索引？
- [ ] 删除任务后，如何清理对象存储中的孤立文件？
- [ ] 把所有运行历史嵌进单个文档，会遇到哪些增长和并发问题？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Data Modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling)（核对日期：2026-10-25）。
