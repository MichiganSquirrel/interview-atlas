---
title: "Database Indexing"
title_en: "Database Indexing"
description: "Database Indexing"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["访问模式 / Query", "索引 / Index", "执行计划 / Plan", "测量 / Measure"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing"
source_hash: "439271e70e9d8bd2c0765c5776c670283cc1bf66acb72957126f27e8733ed569"
---

# Database Indexing

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![数据库索引示意图](../../../../assets/04-database-indexing.svg)

## Core decisions

Indexes reduce the pages read to locate records. B-trees support equality, ranges, and ordering; hash indexes focus on equality; inverted indexes support term search; spatial indexes support location queries. LSM structures trade write, merge, and read costs.

Indexes consume storage and add write maintenance. Composite column order should match filters and ordering. Whether a covering index avoids table access also depends on database-specific visibility conditions.

## Practice: recent jobs for an experiment

```sql
CREATE INDEX jobs_experiment_recent
ON jobs (experiment_id, created_at DESC, id DESC);

SELECT id, state, created_at FROM jobs
WHERE experiment_id = 42
ORDER BY created_at DESC, id DESC LIMIT 20;
```

The index locates one experiment and scans in time order. A query filtering only by `state` may behave differently. Verify scanned rows, sorts, and actual runtime with EXPLAIN. Low-selectivity queries may favor a sequential scan.

## Self-check

- [ ] Why avoid indexing every column?
- [ ] Why is `(a,b)` different from `(b,a)`?
- [ ] Explain trade-offs among write throughput, read latency, and space amplification.

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Database Indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing) (checked 2026-10-25).
