---
title: "强化学习系统知识地图"
title_en: "RL Systems Knowledge Map"
description: "强化学习系统知识地图"
date: "2026-10-25"
tags: ["interview", "rl-systems"]
status: "待复习"
public: true
---

# 强化学习系统知识地图

本页是待填充的复习框架，不代表已有项目经历或已掌握程度。

| 维度 | 需要回答的问题 |
| --- | --- |
| 目标与算法（Objective / Algorithm） | 优化什么目标？优势估计、裁剪、KL 约束如何影响训练？ |
| 数据流（Data Flow） | 提示词 → 采样（Rollout）→ 奖励（Reward）→ 训练批次如何流转？ |
| 系统执行（Execution） | 训练与推理资源如何分配？同步和异步各有什么代价？ |
| 性能（Performance） | 吞吐、GPU 利用率、长尾、显存、通信分别怎么测？ |
| 稳定性（Stability） | 旧策略数据、版本错配、数值异常、奖励投机怎样发现？ |
| 恢复（Recovery） | 检查点、重试、去重与可复现性需要保存什么？ |
| 评估（Evaluation） | 怎样区分奖励提升、泛化改善和评估污染？ |

## 每个知识点的答题模板

定义 → 数学目标或数据流 → 系统约束 → 失败模式 → 可测量证据。

[容量估算](../02-system-design/core-concepts/09-capacity-estimation.md) · [数据建模](../02-system-design/core-concepts/03-data-modeling.md) · [项目深挖](../06-project-deep-dives/deep-dive-template.md) · [模块导航](README.md)
