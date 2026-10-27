---
title: "AI-assisted Software Engineering"
title_en: "AI-assisted Software Engineering"
description: "AI-assisted Software Engineering"
date: "2026-10-25"
tags: ["interview", "ai-engineering"]
status: "待复习"
public: true
source_hash: "c3a15857bd35b7b1ab0d0ff4a5db352bc71471f8a68b05f17bb841b7d8221c97"
---

# AI-assisted Software Engineering

Deliver verifiable software with AI through context preparation, debugging, review, and acceptance checks.

## Study routine

Explain one question without notes before revising it. Record evidence, unverified assumptions, and a next review date.

Progress: review needed → explain → solve independently → handle follow-ups.

## Notes

<!-- AUTO:START -->
- [Practical Delivery & Acceptance Checklist](practical-checklist.md)
<!-- AUTO:END -->

## Minimal Coding Agent example

[The Python example in this module](200lineClaudeCode.py) demonstrates a complete agent loop: the user enters a task, the model emits a single line in the form `tool: tool_name(JSON_arguments)`, Python selects a function from the tool registry and executes it, and a `tool_result(...)` message is added to the conversation so the model can decide what to do next. The inner loop continues the same task until the model returns ordinary text; the outer loop then waits for another user input. This implementation uses a custom text protocol and does not pass native `tools` or `tool_calls` to the API.

The three tools read a file, list a directory, and replace file contents. Paths are resolved relative to the working directory from which the script was launched. `edit_file` replaces only the first match; an empty `old_str` creates or overwrites the entire file. The current implementation has no workspace boundary, tool-call limit, or shared handling for API and file errors. The tool branch also omits the model's tool request from the message history and appends only the execution result. When reading the example, distinguish its current behavior from possible future improvements.

The client reads authentication configuration from the `OPENAI_API_KEY` environment variable, and `load_dotenv()` loads `.env`. Actual configuration and local dependencies are excluded from publication. The source code is preserved as supplied; its Chinese comments help distinguish the responsibilities of context, tool execution, and message history.
