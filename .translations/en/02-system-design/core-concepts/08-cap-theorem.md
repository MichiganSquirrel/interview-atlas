---
title: "CAP & Consistency Trade-offs"
title_en: "CAP & Consistency Trade-offs"
description: "CAP & Consistency Trade-offs"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram_layout: "branch"
diagram: ["网络分区 / Partition", "业务不变量 / Invariant", "拒绝或等待 / Reject", "陈旧响应 / Stale"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem"
source_hash: "a311788c4e1e87dd2a1e026abfd508e5b2adc61a63ee95df7a742ee4d4b03122"
---

# CAP & Consistency Trade-offs

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![CAP 与一致性取舍示意图](../../../../assets/08-cap-theorem.svg)

## Core decisions

CAP concerns the trade-off between consistency and availability during a network partition. Its consistency means linearizability, not ACID consistency. Its availability requires requests received by non-failing nodes to eventually receive responses; it is not an uptime percentage.

CAP does not mean freely choosing any two properties at all times. During a partition, some operations may be rejected or delayed to preserve consistency. Continuing to serve can sacrifice a single real-time global view. PACELC also highlights latency versus consistency when the network is healthy.

## Practice: GPU quotas and progress views

Quota allocation needs explicit concurrency invariants. Reject allocations during a partition if necessary to avoid duplicate commitments. Progress displays can often tolerate stale data and converge later. Choose semantics per operation rather than labeling an entire product CP or AP.

Eventual consistency promises convergence under its assumptions; it does not automatically bound staleness or specify conflict resolution.

## Self-check

- [ ] Explain reads and writes when two regions lose connectivity.
- [ ] Why does using SQL not prove cross-region linearizability?
- [ ] Distinguish read-your-writes from linearizability.

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · CAP & Consistency Trade-offs](https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem) (checked 2026-10-25).
