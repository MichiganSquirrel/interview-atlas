---
title: "Data Modeling"
title_en: "Data Modeling"
description: "Data Modeling"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["查询 / Queries", "实体 / Entities", "约束 / Constraints", "存储 / Storage"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling"
source_hash: "8ed1712b355b96d274fd43d152d6c29bd9efdacd08442f23b08b79edebafe845"
---

# Data Modeling

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![数据建模示意图](../../../../assets/03-data-modeling.svg)

## Core decisions

Work backward from queries and invariants to entities, primary keys, relationships, and constraints. A relational database is a common starting point. Justify document, key-value, or graph models with specific access patterns.

Normalization reduces duplication and update anomalies. Denormalization improves reads through duplication but adds update and repair costs. ACID transactions do not remove the need to choose an isolation level.

## Practice: experiments, jobs, and checkpoints

```sql
experiments(id PRIMARY KEY, owner_id, config_version)
jobs(id PRIMARY KEY, experiment_id, state, attempt)
checkpoints(id PRIMARY KEY, job_id, object_key, step)
```

Keep model weights in object storage; store locations, versions, and checksums in tables. Attempt numbers distinguish retries. Use conditional state transitions so an old worker cannot overwrite a newer attempt. A checkpoint becomes usable only after its payload is complete and its metadata is committed.

## Self-check

- [ ] How would you query an experiment's latest successful checkpoint, and which index supports it?
- [ ] How would you remove orphaned objects after deleting a job?
- [ ] What growth and concurrency problems arise when all history is embedded in one document?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Data Modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling) (checked 2026-10-25).
