---
title: "Caching & Invalidation"
title_en: "Caching & Invalidation"
description: "Caching & Invalidation"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["请求 / Request", "缓存 / Cache", "未命中 / Miss", "数据库 / Database"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/caching"
source_hash: "3df07dbd26bf3673eb1937d5c69afb22ede1171186db958b0cc5a4b74b0ce8df"
---

# Caching & Invalidation

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![缓存策略与失效示意图](../../../../assets/05-caching.svg)

## Core decisions

Caching exchanges storage and consistency complexity for better read latency and lower backend load. Caches can live in clients, CDNs, application processes, or shared services. Cache-aside reads the cache first, loads misses from the database, and fills the cache.

TTL limits residence time but does not independently guarantee an acceptable freshness bound. Eviction differs from expiration. Write-through, write-back, and invalidation strategies have different durability risks.

## Practice: reading training-job status

Terminal job states change rarely and are good cache candidates. Refresh active states according to freshness requirements. Include attempt or version identifiers in keys to avoid stale workers repopulating old values.

| Failure | Response |
| --- | --- |
| Hot entries expire together | Single-flight fetching and expiration jitter. |
| Repeated nonexistent keys | Short-lived negative caching; consider a Bloom filter when appropriate. |
| Cache outage | Rate limits, degradation, and bounded origin concurrency to protect the database. |

## Self-check

- [ ] What if a database update succeeds but invalidation fails?
- [ ] Can a stale reader overwrite a newly cached value?
- [ ] Why can p99 remain poor despite a high hit rate?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Caching & Invalidation](https://www.hellointerview.com/learn/system-design/core-concepts/caching) (checked 2026-10-25).
