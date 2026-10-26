---
title: "Sharding"
title_en: "Sharding"
description: "Sharding"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram_layout: "branch"
diagram: ["分片键 / Key", "路由 / Router", "分片 A / Shard A", "分片 B / Shard B"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/sharding"
source_hash: "ce0602e2e7e431230aae65e730e7cb30b97cb01b7331e69f4c2591a798f7f877"
---

# Sharding

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![数据分片示意图](../../../../assets/06-sharding.svg)

## Core decisions

Sharding distributes data across machines. Partitioning often divides tables inside one database instance. Replication keeps copies and does not by itself distribute primary writes.

Measure whether indexing, query optimization, vertical scaling, or read replicas can solve the bottleneck first. A shard key must balance traffic distribution, locality, and hotspots. Hash, range, and directory routing have different maintenance costs.

## Practice: training logs

Sharding by `experiment_id` keeps experiment queries local, but a huge experiment can create a hot shard. Time buckets or subshards spread writes while increasing read fan-out. Global search may need a separate search index.

Explain expansion through historical migration, incremental replication or dual writes, routing cutover, validation, and rollback. Include cross-shard transactions and global ordering in the cost.

## Self-check

- [ ] If one user generates half of all writes, does hashing the user ID help?
- [ ] How do you merge the latest 20 records from several shards?
- [ ] How do routing-version mismatches cause missed reads or duplicate writes?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding) (checked 2026-10-25).
