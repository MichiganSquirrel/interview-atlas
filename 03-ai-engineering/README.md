---
title: "AI 辅助工程实战"
title_en: "AI-assisted Software Engineering"
description: "AI 辅助工程实战"
date: "2026-10-25"
tags: ["interview", "ai-engineering"]
status: "待复习"
public: true
---

# AI 辅助工程实战

用 AI 完成可验证的工程交付，练习上下文、调试、评审与验收。

## 复习方法

每次选一个问题，先脱稿讲解，再补笔记。记录依据、尚未验证的假设和下一次复习时间。

熟练度：待复习 → 能解释 → 能独立完成 → 能应对追问。

## 本模块资料

<!-- AUTO:START -->
- [实战交付与验收清单](practical-checklist.md)
- [Coding Agent 的双层循环](scratch_note.md)
<!-- AUTO:END -->


## 最小 Coding Agent 实例

[模块内的 Python 示例](200lineClaudeCode.py)展示了一个完整的工具调用循环（Agent Loop）：用户输入任务，模型输出单行 `tool: 工具名(JSON参数)`，Python 从工具注册表（Tool Registry）选择函数执行，再把 `tool_result(...)` 加入对话，让模型决定下一步。内层循环持续处理同一个任务，直到模型返回普通文本；外层循环再等待用户的新输入。这里采用自定义文本协议，代码没有向 API 传入原生 `tools` 或 `tool_calls`。

三个工具分别读取文件、列出目录和替换文件内容。路径相对于启动脚本时的工作目录（Working Directory）解析；`edit_file` 只替换首次匹配，空 `old_str` 会创建或覆盖整个文件。当前实现没有工作区边界限制、调用次数上限或统一的 API 与文件异常处理。工具分支也没有把模型发出的工具请求保存到历史，只追加执行结果；阅读时应区分现有行为和将来可以改进的设计。

客户端从环境变量 `OPENAI_API_KEY` 读取鉴权配置，`.env` 由 `load_dotenv()` 加载；真实配置和本地依赖不会随笔记发布。源码保留原样，中文注释用于对照理解上下文（Context）、工具执行（Tool Execution）和消息历史（Message History）的职责。