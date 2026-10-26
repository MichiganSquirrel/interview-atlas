---
title: "Capacity Estimation & Orders of Magnitude"
title_en: "Capacity Estimation & Orders of Magnitude"
description: "Explicit calculations for requests, storage, bandwidth, concurrency, backlog, and failure headroom."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["负载 / Load", "单位 / Units", "峰值 / Peak", "余量 / Headroom"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know"

source_hash: "4e9609787c46c831f4dfd25fe52761e90fc7464dbc24fd803a6381a2d3dccd26"
---

# Capacity Estimation and Orders of Magnitude

Estimates should support decisions: whether one machine suffices, whether caching helps, how long data can be retained, and whether failure leaves enough capacity. Use assumptions and measurements rather than universal vendor benchmark limits.

![From workload assumptions to peaks and headroom](../../../../assets/09-capacity-estimation.svg)

## Convert demand into work

Daily active users are neither simultaneous users nor requests per second. Estimate operations per user and the service calls, database accesses, and messages each operation creates.

```text
Average requests/s = daily operations / 86,400
Peak requests/s = average requests/s × an explicit peak factor
Backend reads/s ≈ requests/s × reads/request × miss rate
```

Peak factors depend on time zones, scheduled work, events, and tenant skew. Fan-out, retries, and background work increase internal traffic beyond external demand.

## A complete log-ingestion example

Assume 10 million daily records, 2 KB each in decimal units, and a 10× peak. These are illustrative assumptions, not measurements.

| Item | Calculation | Result |
| --- | --- | --- |
| Average ingestion | `10,000,000 / 86,400` | About 116 records/s. |
| Peak ingestion | `116 × 10` | About 1,160 records/s. |
| Daily raw data | `10,000,000 × 2,000 B` | 20 GB/day. |
| Thirty-day raw retention | `20 × 30` | 600 GB. |
| Three raw replicas | `600 × 3` | 1.8 TB. |
| Peak payload bandwidth | `1,160 × 2,000 B/s × 8` | About 18.6 Mb/s. |

Indexes, metadata, headers, replication traffic, backups, and compression remain separate. Three replicas are not three independent historical backups: deletion can propagate to all copies.

## Latency, throughput, and concurrency

Latency measures request duration; throughput measures completed work per time; concurrency measures simultaneous work. They are not interchangeable.

In a stable system, Little's Law uses averages: average in-flight work equals average arrival rate times average time in the system. At 2,000 requests/s and 0.1 s average duration, expect about 200 in-flight requests. Do not substitute p99 or treat an indefinitely growing queue as steady state.

End-to-end p99 is not simply the sum of component p99 values. Fan-out, correlated failures, and queuing affect tails. Allocate budgets and verify the complete path.

## Calculate resource dimensions separately

CPU depends on computation and parallel efficiency. Memory includes resident data, connection buffers, and object overhead. Storage needs capacity, IOPS, bandwidth, and durability analysis. Network traffic includes responses, replication, and cross-region exchange.

At an assumed 32 KiB per active connection, 100,000 connections use about 3.05 GiB for that component alone. This is not a fixed server overhead; TLS, application, and kernel state may add costs. Bandwidth capacity also does not determine small-request throughput when CPU or packet processing dominates.

## Avoid fixed QPS limits

Point reads, joins, large transactions, durable writes, and large responses impose different costs on identical hardware. Indexes, cache state, connections, batching, and contention change results.

Report dataset size, distribution, read/write mix, payload, durability, cache state, latency targets, and errors. Sustainable capacity means throughput meeting those targets, not the highest brief rate before collapse.

## Failure and recovery headroom

A cluster sufficient in normal operation may fail after losing a node or zone. Calculate remaining capacity and reserve room for replication, warmup, backlog recovery, and deployments.

Queues postpone work rather than creating capacity. At 1,500 arrivals/s and 1,200 completions/s, backlog grows by 300/s. Recovery needs processing above new arrivals. Under stable assumptions, drain time is approximately `backlog / (processing rate - arrival rate)`.

## Turn estimates into decisions

Find the tightest resource and compare targeted changes: fewer queries, better indexes, batching, or larger machines. Introduce caching, asynchronous work, or sharding when measurements and growth justify them.

Compare scenarios such as doubled record size or a peak factor rising from 10 to 20. Identify which uncertainty changes the design. Real cloud cost comparisons require current region- and configuration-specific prices.

## Related notes and source

[Indexes](04-database-indexing.md) · [Caching](05-caching.md) · [Sharding](06-sharding.md) · [RL systems](../../04-rl-systems/knowledge-map.md)

Learning reference: [Hello Interview · Numbers to Know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), reviewed through the authenticated written chapter. All workload, connection, and backlog calculations are independent examples with explicit assumptions, not vendor promises.
