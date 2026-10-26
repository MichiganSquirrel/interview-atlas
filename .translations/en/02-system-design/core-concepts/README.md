---
title: "Core Concepts: Complete Topic Index"
title_en: "Core Concepts: Complete Topic Index"
description: "Core Concepts: Complete Topic Index"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
source_hash: "a862f1b43a7d202d121469df94cf3f90655d4a925421b9d0c36299545f40fd2b"
---

# Core Concepts: Complete Topic Index

Nine explanatory chapters are available as continuous reading. All prose is visible without expansion controls, quizzes, or self-checks. Each chapter connects concepts, mechanisms, suitable uses, and trade-offs through concrete examples.

| Chapter | Coverage |
| --- | --- |
| [Networking](01-networking.md) | Request paths, layers, protocols, real-time communication, balancing, regions, and recovery. |
| [API design](02-api-design.md) | Contracts, asynchronous operations, idempotency, pagination, authorization, and evolution. |
| [Data modeling](03-data-modeling.md) | Access patterns, entities, constraints, concurrency, object storage, and lifecycle. |
| [Indexes](04-database-indexing.md) | Pages, B-trees, LSM, composite and covering indexes, plans, and maintenance. |
| [Caching](05-caching.md) | Placement, access patterns, freshness, invalidation races, hotspots, and origin protection. |
| [Sharding](06-sharding.md) | Keys, placement, hotspots, cross-shard operations, and migration. |
| [Consistent hashing](07-consistent-hashing.md) | Remapping, rings, virtual nodes, membership versions, and replication boundaries. |
| [CAP and consistency](08-cap-theorem.md) | Partition behavior, consistency models, and end-to-end read guarantees. |
| [Capacity estimates](09-capacity-estimation.md) | Demand, storage, bandwidth, concurrency, resources, queues, and headroom. |

## Reading order

Networking and APIs → modeling and indexes → caching → sharding and consistent hashing → CAP → estimation. Start with one request, then consider scaling and failure. Individual chapters can also be opened directly.

## Diagrams and offline reading

Each chapter includes an SVG preview. Download the [interactive system-design overview, Chinese](../../../../assets/system-design-map.html) as standalone HTML. The complete pack contains both languages, diagrams, and an Obsidian-ready folder.

## Reading references

All nine written topics were reviewed through the existing authenticated Hello Interview session. These guides are independently organized around system questions with primary documentation and worked examples; they do not transcribe course videos or quizzes. Other patterns, technologies, and design problems are outside this set.

[Hello Interview curriculum](https://www.hellointerview.com/learn/courses/system-design) · [Back to system design](../README.md)
