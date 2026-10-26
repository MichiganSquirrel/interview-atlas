---
title: "Data Modeling"
title_en: "Data Modeling"
description: "Model entities, relationships, transactions, objects, and lifecycle from access patterns and invariants."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["查询 / Queries", "实体 / Entities", "约束 / Constraints", "存储 / Storage"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling"





source_hash: "f21548b985c6e1c96ec18a85782d49a01472d1c79e068358f0f33d55eab4fc5b"
---

# Data Modeling

A data model converts access patterns, business invariants, and lifecycle requirements into executable structures. Database selection, indexes, and sharding should follow from those requirements.

![A path from queries to storage](../../../../assets/03-data-modeling.svg)

## Start with reads, writes, and invariants

A training platform lists experiments by owner, finds recent jobs by experiment, reads successful checkpoints, and retries jobs. Its invariants include ownership, protection against stale attempts, and checkpoint publication only after complete writes.

These requirements are more precise than SQL versus NoSQL. Describe queries, sorting, filters, write frequency, and scale. Decide which constraints belong in the database and which require an application protocol.

## Entities, keys, and relationships

Experiments have many jobs; jobs have many checkpoints. Membership tables can model users belonging to multiple teams. Use stable system identifiers internally rather than mutable email addresses. Natural identifiers can still have uniqueness constraints.

```sql
experiments(id PRIMARY KEY, owner_id, config_version, created_at)
jobs(id PRIMARY KEY, experiment_id, state, active_attempt, version, created_at)
job_attempts(job_id, attempt, worker_id, state, PRIMARY KEY(job_id, attempt))
checkpoints(id PRIMARY KEY, job_id, attempt, step, object_key, state)
```

Separating logical jobs from execution attempts preserves retry history. Real schemas also need foreign keys, non-null constraints, and appropriate uniqueness rather than relying on every caller to enforce rules.

## What different models change

| Model | Suitable access | Cost |
| --- | --- | --- |
| Relational | Relationships, constraints, transactions, and combined queries. | Indexes, contention, and distributed scaling still matter. |
| Document | Nested data commonly read as a bounded aggregate. | Unbounded arrays, duplicate updates, and cross-document consistency. |
| Key-value | Exact-key access for sessions, configuration, or caches. | Arbitrary filters and joins are usually not its strength. |
| Wide-column | Large workloads organized by partition and ordering keys. | Queries must be designed ahead of time; hotspots remain possible. |
| Graph | Workloads dominated by relationship traversal. | Additional storage and query complexity; relationships alone do not justify it. |

A product category does not establish its exact transaction or consistency guarantees. Specify the operations and guarantees of the actual system.

## Normalization and denormalization

Normalization reduces duplication and update anomalies. Denormalization can improve a proven access path, such as storing a latest-job summary with an experiment.

For duplicated views identify the source of truth, update mechanism, and repair process. Asynchronous materialized views reduce read cost but introduce visibility delay and rebuilding. A historical submission-time configuration can be an intentional business fact rather than erroneous duplication.

## Protect concurrent state changes

ACID consistency does not guarantee that every concurrent execution matches application intent. Isolation levels, locks, and conditional writes determine observable behavior. [PostgreSQL's isolation documentation](https://www.postgresql.org/docs/current/transaction-iso.html) distinguishes these guarantees.

```sql
UPDATE jobs
SET state = 'running', version = version + 1
WHERE id = :job_id AND state = 'queued' AND version = :expected_version;
```

Zero updated rows means the record changed, not that acquisition succeeded. Completion should verify attempt numbers or fencing tokens so an expired worker cannot overwrite a newer execution.

## Large objects and publication boundaries

Keep weights, archived logs, and datasets in object storage; record locations, sizes, checksums, versions, and publication state in metadata. Object storage and a database generally do not share a local transaction.

One approach writes to a unique temporary location, validates the object, and then commits availability. Garbage collection removes abandoned objects. Readers consume only published records. Versioning, attempt IDs, and idempotent publication help prevent overwrites and duplicate registrations.

## Access paths and lifecycle

An index on `(experiment_id, created_at, id)` supports recent experiment jobs. Owner-wide queries may require another access path. Sharding by experiment preserves locality but can create a hotspot for a huge experiment.

Retention, archives, logical deletion, physical deletion, and audit records affect the schema. Logical deletion does not reclaim storage. Database and object cleanup require retryable workflows and clear retention boundaries.

## Related notes and source

[Indexes](04-database-indexing.md) · [Sharding](06-sharding.md) · [CAP](08-cap-theorem.md) · [RL systems](../../04-rl-systems/knowledge-map.md)

Learning reference: [Hello Interview · Data Modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling), reviewed through the authenticated written chapter. The jobs, attempts, and checkpoints model is an independent example.
