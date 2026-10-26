---
title: "实战交付与验收清单"
title_en: "Practical Delivery & Acceptance Checklist"
description: "实战交付与验收清单"
date: "2026-10-25"
tags: ["interview", "ai-engineering"]
status: "待复习"
public: true
---

# 实战交付与验收清单

## 一次练习的完整闭环

需求澄清 → 最小实现 → 工具验证 → 人工评审 → 复盘。先定义验收条件（Acceptance Criteria），再让 AI 拆解任务。

- 上下文（Context）：输入、输出、已有接口、运行环境、不可改变的约束。
- 工具（Tools）：文件搜索、运行测试、检查日志与查看差异。
- 调试（Debugging）：复现 → 缩小范围 → 提出假设 → 验证 → 修复。
- 评审（Review）：正确性、失败路径、依赖、凭据处理与可维护性。
- 证据（Evidence）：实际运行结果、尚未覆盖的边界和下一步。

## 练习记录

| 任务 | 时间限制 | 验收条件 | AI 的错误 | 我的修正 | 验证结果 |
| --- | --- | --- | --- | --- | --- |

[API 设计](../02-system-design/core-concepts/02-api-design.md) · [项目深挖](../06-project-deep-dives/deep-dive-template.md) · [模块导航](README.md)
