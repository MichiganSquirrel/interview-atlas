---
title: "Sharding"
title_en: "Sharding"
description: "Shard keys, traffic distribution, cross-shard queries, transaction boundaries, and online migration."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram_layout: "branch"
diagram: ["分片键 / Key", "路由 / Router", "分片 A / Shard A", "分片 B / Shard B"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/sharding"


source_hash: "615788f2ee6e1bf65ebbd31eb9b30fe331aa47586a58ec361e1d3bbdf40ac40a"
---

# Sharding

Sharding distributes a logical dataset across machines to expand capacity or share load. It changes query, transaction, migration, and operational boundaries, not merely the routing formula.

![A shard key routes to different shards](../../../../assets/06-sharding.svg)

## Partitioning, sharding, and replication

Single-instance partitioning creates smaller management units and can help pruning, archiving, and maintenance without adding machines. Sharding usually puts subsets on different machines. Replication copies the same data for resilience or supported read scaling.

They can coexist: shards have replicas and databases can have internal partitions. Read replicas do not automatically remove a primary write hotspot.

## Establish a constraint first

Determine whether storage, IO, CPU, logging, locks, or one hot object limits the system. Query and index changes, pooling, batching, larger machines, caching, or read replicas may suffice.

Shard when expected load, growth, recovery time, or geographic requirements justify it. No universal GB or QPS threshold applies. Backup and restore duration can matter even before throughput is exhausted.

## Choose a key, then a placement rule

A shard key determines the ownership unit. Good keys spread data and activity while keeping frequent operations local. High cardinality alone does not guarantee balanced traffic.

| Rule | Benefit | Cost |
| --- | --- | --- |
| Range | Natural range queries and contiguous management. | Monotonic writes can overload the newest range. |
| Hash | Spreads many distinct keys. | Loses range locality and needs an expansion strategy. |
| Directory | Explicit placement and large-tenant migration. | Requires available, cached, versioned routing metadata. |

AWS's [partition-key guidance](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) emphasizes activity distribution, not only record counts.

## Change the unit of a hotspot

If one experiment generates half the writes, hashing its ID still selects one destination. Splitting logs by `(experiment_id, time_bucket, subshard)` creates independently routable write units.

Reads then need multiple shards and merging. Query clients must discover bucket boundaries and subshard counts. Random suffixes without a read plan merely move the bottleneck.

## Cross-shard queries and transactions

Fan-out queries aggregate partial results. Global recent-20 queries can merge local candidates, but deep pagination, filters, and unavailable shards complicate semantics. Separate secondary indexes add visibility and consistency questions.

Distributed commit can coordinate transactions, or data ownership can keep critical invariants local. Compensating workflows such as sagas do not equal one atomic transaction. Globally unique IDs do not establish every business uniqueness constraint.

## Online expansion is a protocol

One migration approach prepares a target, copies a snapshot, catches up incremental changes, validates, switches routing versions, retains a rollback window, and eventually removes old copies. Define read and write ownership at every stage.

Copy-then-switch can miss concurrent writes. Uncoordinated dual writes can succeed on only one side. Account for duplication, ordering, tombstones, and stale routes, using versions or routing epochs to constrain old owners.

## Managed systems still need modeling

A database may automate physical splits and balancing, but it cannot choose the right application access unit. Hot keys, cross-partition transactions, and secondary indexes remain important. Different managed systems do not necessarily use the same hash-ring placement algorithm; rely on their documented mechanisms.

## Related notes and source

[Data models](03-data-modeling.md) · [Consistent hashing](07-consistent-hashing.md) · [CAP](08-cap-theorem.md) · [Estimation](09-capacity-estimation.md)

Learning reference: [Hello Interview · Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding), reviewed through the authenticated written chapter. The migration reasoning and training-log example are independently developed.
