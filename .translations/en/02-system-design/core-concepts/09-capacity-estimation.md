---
title: "Capacity Estimation & Orders of Magnitude"
title_en: "Capacity Estimation & Orders of Magnitude"
description: "Capacity Estimation & Orders of Magnitude"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["负载 / Load", "单位 / Units", "峰值 / Peak", "余量 / Headroom"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know"
source_hash: "66398a764f9fed6fac3a28366467c893aa974f6dd2d71d5238c8dfedeccc420e"
---

# Capacity Estimation & Orders of Magnitude

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![容量估算与数量级示意图](../../../../assets/09-capacity-estimation.svg)

## Core decisions

Capacity estimates support decisions; single-machine benchmark results are not universal limits. Throughput depends on hardware, workload, object size, indexes, batching, and durability requirements. A fixed database QPS claim lacks necessary context.

Distinguish averages, peaks, and tail latency. State assumptions, units, and headroom before choosing caching, sharding, or asynchronous processing. Revise estimates with measurements.

## Practice: log ingestion

Assume 10 million records per day, each 2 KB in decimal units. Average ingestion is `10,000,000 / 86,400 ≈ 116 records/s`. A 10× peak is about 1,160 records/s. Raw storage is about 20 GB/day, or 600 GB for 30 days. Three replicas require about 1.8 TB before indexes and compression.

Little's Law: in a stable system, average in-flight work equals arrival rate times average time in the system. At 2,000 requests/s and 0.1 s average duration, expect about 200 in-flight requests. Do not substitute p99 for the average.

## Self-check

- [ ] Why must bytes and bits be kept distinct?
- [ ] Can remaining capacity handle the peak after losing a zone?
- [ ] Which assumption is most likely to change the architecture decision?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Capacity Estimation & Orders of Magnitude](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know) (checked 2026-10-25).
