---
title: "Consistent Hashing"
title_en: "Consistent Hashing"
description: "Consistent Hashing"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["哈希键 / Hash key", "哈希环 / Ring", "后继节点 / Successor", "迁移区间 / Move range"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing"
source_hash: "5abc413e13ffe857d902f18a92b39ee676dc9b77d2661444477df5dcf7446960"
---

# Consistent Hashing

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![一致性哈希示意图](../../../../assets/07-consistent-hashing.svg)

## Core decisions

With `hash(key) % N`, changing the node count remaps many keys. Consistent hashing maps keys and nodes onto a hash ring; a common implementation assigns each key to its clockwise successor.

Virtual nodes give each machine multiple ring positions, improving distribution and representing capacity weights. Under ideal uniform distribution, adding one node to N nodes moves roughly `1/(N+1)` of keys; this is not an unconditional workload guarantee.

## Practice: model-metadata cache

A new node takes responsibility for its new ring intervals. A cache can rebuild entries under the new routing. Durable databases also need data migration, routing versions, reads and writes during migration, and replica recovery.

Consistent hashing does not guarantee replica consistency or solve a single hot key. Address hotspots through splitting, replicated reads, or application rate limits.

## Self-check

- [ ] Draw a three-node ring, add a fourth node, and mark moved intervals.
- [ ] How do virtual nodes affect routing metadata and operations?
- [ ] How does failure recovery differ from planned expansion?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · Consistent Hashing](https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing) (checked 2026-10-25).
