---
title: "数据建模"
title_en: "Data Modeling"
description: "从访问模式与业务不变量设计实体、关系、事务、对象存储和生命周期。"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["查询 / Queries", "实体 / Entities", "约束 / Constraints", "存储 / Storage"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling"




source_access: "authenticated-written-article-reviewed"
---

# 数据建模

数据模型不是只列几张表，而是把访问模式（Access Pattern）、业务不变量（Invariant）和数据生命周期转成可执行的结构。数据库选型、索引和分片都应从这些要求出发。

![从查询到存储的建模路径](../../assets/03-data-modeling.svg)

## 先写清读写与不变量

训练平台可能需要按用户列出实验、按实验查询最近任务、读取成功检查点，以及处理任务重试。不变量包括：实验归属明确；旧尝试不能覆盖新尝试的结果；只有写完并确认的检查点才可用于恢复。

这些约束比“使用 SQL 还是 NoSQL”更具体。先给出主要查询、排序、过滤、写入频率与数据规模，再判断哪些约束能由数据库直接维护，哪些需要应用协议。

## 实体、主键和关系

实验与任务通常是一对多，任务与检查点也是一对多；用户与团队可以通过关联表表达多对多。主键（Primary Key）选择稳定的系统标识，避免用可能修改的电子邮箱承担内部身份。自然键（Natural Key）仍可加唯一约束。

```sql
experiments(id PRIMARY KEY, owner_id, config_version, created_at)
jobs(id PRIMARY KEY, experiment_id, state, active_attempt, version, created_at)
job_attempts(job_id, attempt, worker_id, state, PRIMARY KEY(job_id, attempt))
checkpoints(id PRIMARY KEY, job_id, attempt, step, object_key, state)
```

这里把逻辑任务和执行尝试分开，同一任务重试不会丢掉先前执行历史。实际建表时还应添加外键、非空约束和必要的唯一约束，而不是让每个调用方自行记住规则。

## 不同数据模型改变了哪些操作

| 模型 | 适合的访问 | 要承担的代价 |
| --- | --- | --- |
| 关系型（Relational） | 有明确关系、约束、事务和组合查询的数据。 | 高负载下仍要处理索引、锁竞争和分布式扩展。 |
| 文档型（Document） | 经常整体读取、结构嵌套且可合理聚合的数据。 | 无界数组、重复字段更新和跨文档一致性。 |
| 键值（Key-value） | 明确键查找，例如会话、配置或缓存。 | 任意筛选和关联查询通常不是其强项。 |
| 宽列（Wide-column） | 围绕分区键、按排序键读取的大规模数据。 | 需要提前设计查询模式，避免热分区。 |
| 图（Graph） | 路径遍历本身是核心工作负载的关系数据。 | 多一套存储与查询复杂度，不能仅因“有关联”就选择。 |

产品名称不直接等于一致性或事务能力。应说明具体数据库提供哪些操作与保证，而不是声称某一整类数据库都不能做事务。

## 规范化与反规范化

规范化（Normalization）减少重复和更新异常，例如用户信息只存一份，任务保存 `owner_id`。反规范化（Denormalization）则针对实际读取成本增加冗余，例如在实验列表保存最近任务的摘要。

反规范化之后要回答三个问题：哪一份是事实源（Source of Truth）、由什么机制更新副本、失败后如何重建。异步物化视图（Materialized View）可以减轻读取成本，但会产生可见延迟和修复任务。历史快照中的“提交时配置”不一定是需要纠正的冗余，它可能是有意保留的业务事实。

## 用条件更新保护并发状态

ACID 的一致性并不意味着所有并发执行都会得到期望结果。隔离级别（Isolation Level）、锁与条件更新决定应用看到和修改什么状态。[PostgreSQL 的隔离文档](https://www.postgresql.org/docs/current/transaction-iso.html)区分了这些行为。

```sql
UPDATE jobs
SET state = 'running', version = version + 1
WHERE id = :job_id AND state = 'queued' AND version = :expected_version;
```

受影响行数为零表示记录已变化，调用方不能假定领取成功。工作进程完成时还应验证尝试编号或栅栏令牌（Fencing Token），防止超时的旧工作进程覆盖新执行。

## 大对象与元数据的提交边界

权重、日志归档和数据集通常放对象存储，数据库保存位置、大小、校验和、版本和发布状态。对象存储与数据库通常不共享一个本地事务，因此“文件上传成功”和“元数据提交成功”必须分开处理。

可先把文件写入唯一的临时位置，校验完成后再提交可用状态；中途失败留下的对象通过垃圾回收清理。读取者只使用已发布的记录。对象版本、尝试编号和幂等发布有助于避免覆盖与重复登记。

## 索引、分片与生命周期一起考虑

“某实验最近任务”可以使用 `(experiment_id, created_at, id)` 索引；“某用户全部任务”可能需要另一种访问路径。以实验编号分片能保持局部查询，却可能让超大实验成为热点。

保留期限（Retention）、归档、逻辑删除、硬删除和审计记录也会影响模型。逻辑删除不等于存储已经回收；清理数据库记录与清理对象需要可重试流程和保留边界。模型应在这些情况下仍能说明每份数据由谁管理。

## 关联与来源

[索引](04-database-indexing.md) · [分片](06-sharding.md) · [CAP](08-cap-theorem.md) · [强化学习系统](../../04-rl-systems/knowledge-map.md)

学习入口：[Hello Interview · Data Modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling)（已登录核对书面章节）。任务、尝试与检查点模型为本页独立示例。
