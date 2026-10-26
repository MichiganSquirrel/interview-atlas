---
title: "容量估算与数量级"
title_en: "Capacity Estimation & Orders of Magnitude"
description: "容量估算与数量级"
date: "2026-10-25"
tags: ["interview", "system-design"]
status: "待复习"
public: true
diagram: ["负载 / Load", "单位 / Units", "峰值 / Peak", "余量 / Headroom"]
source: "https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know"
---

# 容量估算与数量级

> 范围：基于公开可访问的原文和主题目录整理；以下面试推演与自测为原创练习，不复刻 Premium 视频、测验或受限正文。

![容量估算与数量级示意图](../../assets/09-capacity-estimation.svg)

## 核心判断

容量估算（Capacity Estimation）用来支持决策，不能把单机性能背成通用上限。吞吐取决于硬件、负载、对象大小、索引、批处理和持久性要求；“某数据库固定支持多少 QPS”缺少必要前提。

先区分平均值、峰值和尾延迟。写出假设、单位与余量（Headroom），再判断是否需要缓存、分片或异步处理。数字必须能由实测校正。

## 面试推演：日志写入

假设每天 1,000 万条、每条 2 KB（十进制），平均写入约 `10,000,000 / 86,400 ≈ 116 条/秒`；峰值取 10 倍约 1,160 条/秒；原始数据约 20 GB/天。保留 30 天约 600 GB，三副本约 1.8 TB，尚未包含索引和压缩。

利特尔定律（Little's Law）：稳定系统中，平均在途请求数约为到达率乘平均停留时间。2,000 请求/秒、平均 0.1 秒，对应约 200 个在途请求；不能代入 p99 作为平均值。

## 自测

- [ ] 为什么字节（Byte）和比特（bit）不能混算？
- [ ] 单区故障后，剩余容量能否承担峰值？
- [ ] 哪个假设变化最可能改变架构结论？

## 相关笔记

[模块导航](../README.md) · [Core Concepts 总览](README.md)

来源：[Hello Interview · Capacity Estimation & Orders of Magnitude](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know)（核对日期：2026-10-25）。
