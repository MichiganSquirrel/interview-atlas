---
title: "API Design"
title_en: "API Design"
description: "API Design"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["资源 / Resource", "契约 / Contract", "鉴权 / Auth", "幂等 / Idempotency"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/api-design"
source_hash: "fe07baf0670cc792e472a35233bb5fd81c3651d7663f4d844d30ca006f48998a"
---

# API Design

> Scope: concise notes based on the publicly accessible article and topic outline. Practice scenarios and self-checks are original; Premium videos, quizzes, and restricted text are not reproduced.

![API 设计示意图](../../../../assets/02-api-design.svg)

## Core decisions

Identify resources and access patterns before selecting a protocol. REST fits ordinary resource operations, GraphQL lets clients select fields, and gRPC suits service calls with explicit contracts.

Idempotency means repeated execution leaves the same business state; response codes need not match. PUT and DELETE have idempotent semantics. POST can implement business idempotency with a key; PATCH depends on the operation.

## Practice: submit a training job

```http
POST /training-jobs
Idempotency-Key: client-generated-key

{"dataset_id":"ds-42","config_version":"v3"}
```

Return `202 Accepted`, a job identifier, and a status location. Use `GET /training-jobs/{id}` for progress. Bind each idempotency key to the caller and request digest to detect incompatible reuse. Authorize using server-verified identity, rather than a client-provided user ID.

Use cursor pagination for lists. Include a unique identifier in the ordering to break timestamp ties.

## Self-check

- [ ] A request commits but the client times out. How does retry avoid creating a second job?
- [ ] Explain when to return 400, 401, 403, 404, 409, and 429.
- [ ] How can concurrent inserts cause skips or duplicates with offset pagination?

## Related notes

[Module index](../README.md) · [Core Concepts overview](README.md)

Source: [Hello Interview · API Design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design) (checked 2026-10-25).
