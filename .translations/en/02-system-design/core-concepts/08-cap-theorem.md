---
title: "CAP & Consistency Trade-offs"
title_en: "CAP & Consistency Trade-offs"
description: "CAP, linearizability, session guarantees, replica read paths, and operation-specific failure behavior."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram_layout: "branch"
diagram: ["网络分区 / Partition", "业务不变量 / Invariant", "拒绝或等待 / Reject", "陈旧响应 / Stale"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem"

source_hash: "3ae1de110474af99a243f863b723de81edcb19a33014cf19ce7b4d76b7c52af2"
---

# CAP and Consistency Trade-offs

CAP explains incompatible guarantees for distributed data during a network partition. Use it to specify failure behavior for particular reads and writes rather than labeling an entire product CP or AP.

![Select partition behavior from business invariants](../../../../assets/08-cap-theorem.svg)

## Define the terms

CAP consistency commonly means linearizability: operations appear to take effect between invocation and response while respecting real-time order. A read starting after a successful write cannot return a value superseded by it.

Availability requires requests received by non-failing nodes to eventually obtain corresponding operation results. Indefinite waiting or universal errors do not satisfy it. It is not monthly uptime and does not itself specify a fixed response-time bound.

A partition prevents reliable communication between groups of nodes. Real systems cannot simply choose never to experience one. Without a partition, CAP does not require sacrificing either consistency or availability.

## A two-region example

Suppose US and European replicas each show one remaining GPU allocation. During a partition, each receives a request. If both promise success, they can overcommit. If an isolated region waits or rejects because it cannot confirm ownership, those operations lose availability.

Consistency-first does not necessarily stop every service. A majority protocol may continue writes on one side while an isolated minority stops committing. The result depends on the protocol, assumptions, and read path. Drawing a leader alone does not prove strong consistency.

## Choose by operation

| Operation | Invariant | Possible partition behavior |
| --- | --- | --- |
| Allocate the last GPU quota | No duplicate resource commitment. | Only an authorized owner commits; others wait or fail. |
| Display progress | Brief staleness is acceptable. | Return known state with time or version information. |
| Read a public model description | Older content is acceptable. | Serve a local replica and update later. |
| Publish a checkpoint | Incomplete objects must not become usable. | Control visibility through a publication protocol. |

Specify affected records, operations, and invariants. A broad statement such as “the whole system is strongly consistent because it handles money” is insufficient.

## Distinguish consistency models

Linearizability concerns real-time order within its specified scope. Serializability makes transaction effects equivalent to some serial execution. Neither automatically implies the other. Strict serializability additionally respects real time.

Read-your-writes and monotonic reads provide session guarantees rather than global linearizability. Eventual consistency converges after writes stop under required communication and repair assumptions; it does not inherently bound convergence time or choose conflict resolution.

ACID consistency concerns valid states and constraints, not CAP's C. SQL, NoSQL, transactions, and replication are not standalone proofs of cross-region guarantees.

## Replication, quorums, and read paths

Synchronous replication coordinates before acknowledgment. Asynchronous replication can return earlier while replicas lag. Leader reads, committed versions, and failover durability affect what clients observe.

`R + W > N` makes read and write sets overlap, but overlap alone does not prove linearizability. Concurrent writes, version rules, failed operations, membership changes, and recovery still need a correct protocol.

Access paths can differ. [DynamoDB's consistency documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) distinguishes tables and local versus global secondary indexes. A strong option on the base table does not establish identical guarantees elsewhere.

## Latency without partitions

PACELC highlights availability versus consistency under partitions and coordination latency versus consistency in normal operation. Cross-continent confirmation introduces network waiting, but implementation details still determine guarantees.

The full client path matters: a strongly consistent database hidden behind an old cache can still expose stale API results. Consider caching, sessions, replication, and failover together.

## Related notes and source

[Caching](05-caching.md) · [Data modeling](03-data-modeling.md) · [Sharding](06-sharding.md)

Learning reference: [Hello Interview · CAP Theorem](https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem), reviewed through the authenticated written chapter. Quota allocation and read-path reasoning provide an independent explanation.
