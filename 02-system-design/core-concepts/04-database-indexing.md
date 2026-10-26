---
title: "数据库索引"
title_en: "Database Indexing"
description: "从数据页与执行计划理解 B-tree、LSM、复合索引、覆盖索引和专用索引。"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["访问模式 / Query", "索引 / Index", "执行计划 / Plan", "测量 / Measure"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing"



source_access: "authenticated-written-article-reviewed"
---

# 数据库索引

索引（Index）是一条额外维护的访问路径。它的价值是减少查询需要检查的数据、读取的数据页或执行的排序；代价是占用空间、缓存和写入维护资源。评价索引应从具体查询开始，而不是给每个字段都创建一个。

![索引设计与验证](../../assets/04-database-indexing.svg)

## 从数据页理解索引的收益

表数据以页组织，数据库把所需页读入内存再处理。没有可用索引时，可能需要扫描很多页；索引先缩小候选记录，再访问必要的表数据。缓存命中、顺序读取和随机读取的成本不同，因此不能把一次逻辑查找直接等同于一次物理磁盘操作。

返回整张表的大部分记录时，顺序扫描（Sequential Scan）可能比通过索引逐条回表更划算。查询优化器会综合选择性、统计信息、数据分布和成本选择执行计划。

## B-tree 与复合索引

B-tree 通过有序的多分支结构支持等值、范围和排序。它的高度通常比较小，但真实延迟还取决于数据是否在缓存、是否回表和返回多少记录。

```sql
CREATE INDEX jobs_by_experiment_recent
ON jobs (experiment_id, created_at DESC, id DESC);

SELECT id, state, created_at
FROM jobs
WHERE experiment_id = 42
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

这个顺序先定位实验，再沿目标顺序取记录。若查询改为只过滤时间，访问方式就不同。设计列序应依据等值条件、范围条件、排序和实际数据分布，不能只背“选择性最高的放第一列”。某些数据库能使用跳跃扫描等优化，最左前缀也不应被说成任何实现都绝对不能越过的规则。

## 覆盖、部分和表达式索引

覆盖索引（Covering Index）包含查询所需字段，可能减少回表。在 PostgreSQL 中，可以使用 `INCLUDE (state)` 存放返回列；能否真正执行高效的仅索引扫描（Index-only Scan），还取决于可见性信息等条件。

部分索引（Partial Index）只保存满足条件的记录，例如活跃任务。它适合小而重要的子集，但查询条件需要能匹配该条件。表达式索引（Expression Index）可以支持 `lower(email)` 等查询；仅对原字段建普通索引不意味着任意函数条件都能直接利用它。相关机制见 [PostgreSQL 的索引文档](https://www.postgresql.org/docs/current/indexes.html)。

## LSM 的写入与合并

日志结构合并树（Log-structured Merge Tree，LSM）通常把写入先记录到写前日志（WAL）和内存结构，再刷新为有序磁盘文件（SSTable）。后台合并（Compaction）整理多个文件和旧版本。具体顺序与持久性以数据库配置为准。

这样可把部分随机更新转换成批量写入，但读取可能要检查多个层和文件；布隆过滤器（Bloom Filter）可跳过不可能包含某键的文件。合并带来额外读写和后台资源消耗。比较 B-tree 和 LSM 时，应同时讨论读放大、写放大、空间放大及尾延迟，不能把它们简化成“一个只读、一个只写”。

## 哈希、倒排与空间索引

| 结构 | 主要解决的问题 | 关键限制 |
| --- | --- | --- |
| 哈希索引（Hash Index） | 根据完整键做等值定位。 | 不保留一般排序关系，不能直接支持范围或有序扫描。 |
| 倒排索引（Inverted Index） | 把词项映射到包含它的文档集合。 | 分词、相关性、更新可见性和索引维护都需要设计。 |
| 空间索引（Spatial Index） | 根据空间邻近和包围关系缩小候选。 | 候选过滤后通常还需要精确几何判断。 |

Geohash 用空间网格编码位置，邻近区域可能跨编码边界，查询需要覆盖相邻格子。四叉树（Quadtree）递归细分二维区域；R-tree 家族用包围区域组织对象。PostGIS 可使用基于 GiST 的空间索引；“知道经纬度就给两列分别建普通索引”并不自动得到高效半径检索。

## 索引为什么会拖慢写入

新增、更新和删除可能同时修改多个索引，增加日志、页维护、缓存压力和存储。把经常变化的宽字段塞进覆盖索引尤其可能得不偿失。唯一索引还能参与约束检查，不能只按读取收益随意删除。

监测索引使用情况、维护成本和实际查询模式，比固定规定“每张表最多几个索引”更有意义。线上建索引的方法还要考虑锁、额外空间和失败后的清理。

## 用执行计划核实，而不是猜测

`EXPLAIN` 展示规划，`EXPLAIN ANALYZE` 会实际执行语句并报告观测结果；对写语句或昂贵查询不能把它当作无副作用的检查。

观察扫描方式、估算行数与实际行数的差距、过滤掉的行数、排序与临时文件、缓存命中和磁盘读取。若估计与实际差异很大，应先检查统计信息和数据倾斜。索引让一个查询更快，不代表整个系统在写入压力和冷缓存条件下也更快。

## 关联与来源

[API 查询](02-api-design.md) · [数据模型](03-data-modeling.md) · [缓存](05-caching.md) · [分片](06-sharding.md)

学习入口：[Hello Interview · Database Indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing)（已登录核对书面章节）。本页围绕查询执行与维护成本独立组织，不复刻课程中的图表或示例。
