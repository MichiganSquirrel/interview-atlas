---
title: "Database Indexing"
title_en: "Database Indexing"
description: "Pages, plans, B-trees, LSM, composite and covering indexes, and specialized access paths."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["访问模式 / Query", "索引 / Index", "执行计划 / Plan", "测量 / Measure"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing"




source_hash: "6a5d66f8689f6ffa5d9f42ddaea73bf906a958c099210ac010fa9f56dadb01fd"
---

# Database Indexing

An index is an additional maintained access path. It can reduce examined records, accessed pages, and sorting, while consuming storage, cache, and write resources. Begin with a concrete query rather than indexing every field.

![Designing and validating an index](../../../../assets/04-database-indexing.svg)

## Pages, scans, and selectivity

Tables are organized into pages processed in memory. An index narrows candidate records before necessary table access. Cache hits, sequential access, and random access differ, so one logical lookup does not imply one physical disk operation.

When a query returns much of a table, a sequential scan can beat many index-directed table fetches. Optimizers consider selectivity, statistics, distribution, and estimated costs.

## B-trees and composite order

B-trees maintain ordered branching structures for equality, ranges, and ordering. Small tree height alone does not determine latency: caching, table fetches, and result count still matter.

```sql
CREATE INDEX jobs_by_experiment_recent
ON jobs (experiment_id, created_at DESC, id DESC);

SELECT id, state, created_at
FROM jobs
WHERE experiment_id = 42
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

This index locates an experiment and follows the requested order. Time-only filtering is a different access path. Choose order from equality, range, ordering, and real distribution, not a universal “most selective first” rule. Some engines support skip-scan optimizations, so left-prefix limitations should not be stated as absolute for every implementation.

## Covering, partial, and expression indexes

Covering indexes include returned fields and can reduce table access. PostgreSQL's `INCLUDE (state)` adds a payload column, but efficient index-only scans also depend on visibility information.

Partial indexes retain a qualifying subset, such as active jobs, and require compatible query predicates. Expression indexes can support `lower(email)`; a normal index does not automatically accelerate arbitrary expressions. See [PostgreSQL's index documentation](https://www.postgresql.org/docs/current/indexes.html).

## LSM writes and compaction

LSM engines typically record writes in a WAL and memory structure before flushing sorted files. Compaction merges files and obsolete versions; exact ordering and durability depend on the implementation and configuration.

Batching can replace some random updates, but reads may inspect several files or levels. Bloom filters skip files that cannot contain a key. Compaction consumes background resources. Compare read, write, and space amplification and tail latency rather than calling B-trees read-only or LSM write-only.

## Specialized structures

| Structure | Purpose | Limitation |
| --- | --- | --- |
| Hash index | Exact-key lookup. | Does not preserve general ordering for ranges or sorted scans. |
| Inverted index | Map terms to documents containing them. | Tokenization, relevance, visibility, and updates require design. |
| Spatial index | Narrow candidates by proximity or bounding regions. | Usually needs a precise geometric check after filtering. |

Geohash encodes spatial cells, but nearby locations can cross boundaries, requiring neighboring cells. Quadtrees recursively divide space; R-tree families organize bounding regions. PostGIS can use GiST-based indexes. Separate ordinary latitude and longitude indexes do not automatically make radius searches efficient.

## Write and maintenance costs

Inserts, updates, and deletes can maintain several indexes, adding logs, cache pressure, and storage. Wide frequently changed covering fields can be costly. Unique indexes also enforce constraints and cannot be removed based solely on read usage.

Observe use and maintenance costs instead of prescribing a fixed maximum index count. Online creation must consider locking, extra space, and cleanup after failures.

## Verify execution

`EXPLAIN` displays a plan. `EXPLAIN ANALYZE` actually executes the statement, so writes and expensive queries are not harmless inspections.

Check scans, estimated versus actual rows, filtered rows, sorts, temporary files, cache hits, and physical reads. Large estimate errors suggest statistics or skew problems. A faster individual query does not prove better overall performance under writes or cold caches.

## Related notes and source

[API queries](02-api-design.md) · [Data models](03-data-modeling.md) · [Caching](05-caching.md) · [Sharding](06-sharding.md)

Learning reference: [Hello Interview · Database Indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing), reviewed through the authenticated written chapter. This guide is independently organized around execution and maintenance costs.
