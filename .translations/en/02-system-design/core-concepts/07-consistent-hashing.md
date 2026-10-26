---
title: "Consistent Hashing"
title_en: "Consistent Hashing"
description: "Modulo remapping, rings, virtual nodes, membership versions, replicas, and hotspots."
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["哈希键 / Hash key", "哈希环 / Ring", "后继节点 / Successor", "迁移区间 / Move range"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing"


source_hash: "fd1a0b9355853de578fd2cd91b715a3a688eeb98080ac652a7a697002f9c2b0a"
---

# Consistent Hashing

Consistent hashing reduces key reassignment when cluster membership changes. It is a placement and routing method, not a protocol for replica agreement, durability, or recovery.

![From a key to a ring and owner](../../../../assets/07-consistent-hashing.svg)

## Why direct modulo complicates expansion

For a fixed cluster, `hash(key) % N` is simple. Changing N to N+1 remaps many keys. Caches can experience widespread misses; persistent stores need movement and compatibility with old locations.

The issue is coupling ownership directly to physical node count, not modulo itself. Fixed logical partitions mapped separately to machines provide another way to reduce that coupling.

## Ring ownership

Place keys and nodes in a circular hash space. A common rule assigns a key to the first clockwise node, wrapping around at the end.

Suppose `A=10, B=50, C=90`. Key 30 belongs to B, key 70 to C, and key 95 wraps to A. Adding `D=35` transfers `(10,35]` from B to D without changing other intervals. These small integer positions illustrate the rule.

```text
Before: 10(A) ---- 30(key) -------- 50(B) -------- 90(C)
After:  10(A) ---- 30(key) -- 35(D) -- 50(B) ----- 90(C)
```

With ideal uniform distribution and equal weights, adding a node takes roughly `1/(N+1)` of keys on average. This is not an exact guarantee for each expansion, byte volume, or request load.

## Virtual nodes

One position per machine can leave a successor overloaded after a failure. Virtual nodes assign several distributed positions to each physical machine, spreading transferred intervals. More positions can represent greater capacity.

Costs include routing metadata and migration management. Virtual nodes cannot split one hot key, and balanced key counts need not imply balanced memory consumption.

## Membership and routing versions

Clients, proxies, or servers need a membership view and ring version. Different versions can send the same key to different owners.

Migration can involve forwarding, redirects, or controlled reads from old and new locations. Writes need explicit ownership and cutover rules. Removing a node solely on a local timeout can mistake a partition for failure and create competing writers.

## Placement versus recovery

Placement determines where data belongs; replication determines where additional copies exist. Replicas should span physical machines and relevant failure domains. Several virtual nodes on one machine are not independent backups.

Failed caches can rebuild from a source of truth. Durable data needs existing replicas or another recovery source. Expansion still needs historical copying, change catch-up, and validation.

## Hotspots and alternative placement

Hot keys may need local caches, replicated reads, splitting, or rate limiting, each with separate consistency and invalidation decisions. Alternatives such as rendezvous hashing also reduce remapping.

Redis Cluster illustrates why product details matter: it maps 16,384 fixed hash slots onto nodes and migrates slots, rather than directly using this virtual-node ring. The [Redis Cluster specification](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/) documents slots and redirects.

## Related notes and source

[Sharding](06-sharding.md) · [Caching](05-caching.md) · [CAP](08-cap-theorem.md)

Learning reference: [Hello Interview · Consistent Hashing](https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing), reviewed through the authenticated written chapter. The integer-ring example and routing-version discussion are independent explanations.
