---
title: "API 设计"
title_en: "API Design"
description: "从资源契约讲清 HTTP 语义、异步任务、幂等、分页、权限和接口演进。"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["资源 / Resource", "契约 / Contract", "鉴权 / Auth", "幂等 / Idempotency"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/api-design"




source_access: "authenticated-written-article-reviewed"
---

# API 设计

接口契约（API Contract）要明确谁能对哪些资源做什么、输入如何表达、结果与错误如何返回，以及网络重试会产生什么影响。下面用一个训练平台贯穿说明，重点是可实现的业务语义。

![API 设计的主要决策](../../assets/02-api-design.svg)

## 从资源与操作开始

先识别实验（Experiment）、任务（Training Job）和检查点（Checkpoint）。资源身份放在路径中，可选筛选放查询参数，创建或修改的内容放请求体：

```http
POST /training-jobs
GET /training-jobs/job-42
GET /training-jobs?experiment_id=exp-7&state=running&limit=20
POST /training-jobs/job-42/cancellations
```

取消可以建模为取消请求资源，也可以使用明确的 RPC 操作。URL 是否“漂亮”不如取消究竟是同步完成、接受后异步执行，还是可能被重复提交重要。

## 方法与状态码表达什么

| 方法 | 常见语义 | 重试时要注意 |
| --- | --- | --- |
| GET | 读取资源，应当是安全操作。 | 响应可能变化，但不应因此产生业务副作用。 |
| POST | 创建资源或提交操作。 | 默认不保证幂等，需要应用去重。 |
| PUT | 在指定地址完整替换或创建资源。 | 相同请求应有幂等效果。 |
| PATCH | 局部修改。 | “设为某值”和“追加一次”具有不同幂等性质。 |
| DELETE | 删除资源。 | 最终状态可幂等，重复请求的状态码可以不同。 |

创建已经完成可返回 `201 Created`；只是接受了异步工作可返回 `202 Accepted` 和状态查询位置。`400` 表示输入问题，`401` 表示缺少有效身份，`403` 表示权限不足，`409` 表示资源状态冲突，`429` 表示请求受到限流。状态码只表达类别，业务错误还应有稳定的错误标识。

## 异步操作需要可观察的状态

任务创建接口可以立即返回任务编号、当前状态与 `Location`。之后查询返回 `queued → running → succeeded/failed/cancelled` 中的状态。取消请求已接受，不等于 GPU 工作进程已经停止。

```json
{
  "id": "job-42",
  "state": "queued",
  "attempt": 1,
  "status_url": "/training-jobs/job-42"
}
```

状态和尝试编号应来自同一份受控数据。失败原因、是否可重试、结果位置也属于契约，不应让客户端从日志文字里猜测。

## 幂等键要和业务提交绑定

客户端在一次逻辑创建开始时生成幂等键（Idempotency Key），网络重试继续使用同一个键。服务端按调用者、接口和键记录请求摘要与处理结果；同键不同参数应返回冲突，不能悄悄复用旧结果。

最容易遗漏的是原子性：如果任务创建成功后，进程在保存去重结果前崩溃，重试仍可能创建第二个任务。可以在同一事务中保存幂等记录和任务记录，并通过唯一约束处理并发请求。进行中的重复请求、去重记录的保留期和过期后的语义都需要定义。

## 分页、排序与查询成本

偏移分页（Offset Pagination）适合稳定的小列表或需要按页跳转的界面，但大偏移可能扫描大量数据，列表变动也可能导致重复与漏读。游标分页（Cursor Pagination）保存排序边界，适合持续增长的数据。

```sql
WHERE owner_id = :owner
  AND (created_at, id) < (:last_time, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

时间相同的记录需要唯一编号打破平局。游标还应绑定筛选条件和排序方向；游标分页本身不保证跨页快照一致性。服务端应限制 `limit`、允许的筛选字段与排序组合，以免接口暴露无法有效执行的任意查询。[API 参数与底层索引要一起设计](04-database-indexing.md)。

## 身份、授权和错误格式

认证（Authentication）回答“你是谁”，授权（Authorization）回答“能否操作这个资源”。即使 JWT 验证成功，读取 `job-42` 时仍应检查任务归属或团队权限，不能仅相信请求中的 `owner_id`。

错误响应使用稳定的机器标识和可读信息，例如 `{"error":{"code":"JOB_ALREADY_TERMINAL","message":"Job cannot be cancelled"}}`。避免返回内部堆栈或凭据。限流可按用户、租户和接口成本分别计算；重试提示必须和客户端的总截止时间一起考虑。

## GraphQL、gRPC 与兼容演进

GraphQL 把数据形状的选择交给客户端，适合多个客户端访问重叠但不同的数据；后台要限制查询深度和成本、批量加载关联数据，并在解析器中执行资源级授权。一个 GraphQL 请求也可能触发许多数据库查询。

gRPC 用服务方法与消息类型表达契约，适合内部训练调度器和执行器通信。应明确截止时间、取消、流式响应和错误映射。选择二进制格式并不自动解决服务端计算或数据库瓶颈。

演进时，增加可选字段通常比改字段含义更容易兼容，但仍取决于客户端解析方式。删除字段、改变排序或错误语义都可能破坏客户端；版本号不能替代清晰的弃用和迁移规则。

## 关联与来源

[网络基础](01-networking.md) · [数据建模](03-data-modeling.md) · [索引](04-database-indexing.md) · [模块导航](../README.md)

学习入口：[Hello Interview · API Design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design)（已登录核对书面章节）。上面的训练任务接口、事务去重和查询示例为独立组织的讲解。
