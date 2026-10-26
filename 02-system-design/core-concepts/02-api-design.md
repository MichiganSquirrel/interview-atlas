---
title: "API 设计"
title_en: "API Design"
description: "API 设计"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["资源 / Resource", "契约 / Contract", "鉴权 / Auth", "幂等 / Idempotency"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/api-design"
---

# API 设计

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![API 设计示意图](../../assets/02-api-design.svg)

## 核心判断

先确认资源（Resource）和访问方式，再选协议。REST 适合常见资源操作；GraphQL 适合客户端按需选择字段；gRPC 适合有明确契约的服务间调用。

幂等性（Idempotency）指重复执行后的业务状态一致，不要求每次返回相同状态码。PUT 和 DELETE 具备幂等语义；POST 可以通过幂等键获得业务幂等；PATCH 取决于操作内容。

## 面试推演：提交训练任务

```http
POST /training-jobs
Idempotency-Key: client-generated-key

{"dataset_id":"ds-42","config_version":"v3"}
```

返回 `202 Accepted`、任务标识与状态查询位置；`GET /training-jobs/{id}` 查询进度。幂等键必须绑定调用者和请求摘要，避免同键不同请求。鉴权（Authorization）依据服务端身份，不能信任请求体里的用户编号。

列表用游标分页（Cursor Pagination）；排序字段加唯一标识，避免时间相同导致翻页不稳定。

## 自测

- [ ] 请求已提交但客户端超时，重试如何避免创建两个任务？
- [ ] 说明 400、401、403、404、409、429 的适用情况。
- [ ] 分页期间新增数据时，偏移分页（Offset Pagination）可能怎样漏读或重读？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · API Design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design)（核对日期：2026-10-25）。
