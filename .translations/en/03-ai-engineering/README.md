---
title: "AI-assisted Software Engineering"
title_en: "AI-assisted Software Engineering"
description: "AI-assisted Software Engineering"
date: "2026-10-25"
tags: ["interview", "ai-engineering"]
status: "待复习"
public: true
source_hash: "ce8ad86a40040ea19d6a36fa19c041bb0e4f5b39ed14463336f413ac3c4d5a85"
---

# AI-assisted Software Engineering

Deliver verifiable software with AI through context preparation, debugging, review, and acceptance checks.

## Study routine

Explain one question without notes before revising it. Record evidence, unverified assumptions, and a next review date.

Progress: review needed → explain → solve independently → handle follow-ups.

## Notes

<!-- AUTO:START -->
- [Practical Delivery & Acceptance Checklist](practical-checklist.md)
- [The Two Loops of a Coding Agent](scratch_note.md)
<!-- AUTO:END -->

## Minimal Coding Agent example

[The Python example in this module](200lineClaudeCode.py) demonstrates a complete agent loop: the user enters a task, the model emits a single line in the form `tool: tool_name(JSON_arguments)`, Python selects a function from the tool registry and executes it, and a `tool_result(...)` message is added to the conversation so the model can decide what to do next. The inner loop continues the same task until the model returns ordinary text; the outer loop then waits for another user input. This implementation uses a custom text protocol and does not pass native `tools` or `tool_calls` to the API.

The three tools read a file, list a directory, and replace file contents. Paths are resolved relative to the working directory from which the script was launched. `edit_file` replaces only the first match; an empty `old_str` creates or overwrites the entire file. The current implementation has no workspace boundary, tool-call limit, or shared handling for API and file errors. The tool branch also omits the model's tool request from the message history and appends only the execution result. When reading the example, distinguish its current behavior from possible future improvements.

The current module source calls `execute_llm_call()` from the inner loop. Its client reads authentication configuration from `OPENAI_API_KEY` when the module is loaded and uses the SDK's default OpenAI endpoint. `load_dotenv()` loads `.env`. Actual configuration and local dependencies are excluded from publication. The source code is preserved as supplied; its Chinese comments help distinguish the responsibilities of context, tool execution, and message history.


[The two-loop note](scratch_note.md) contains an improved implementation: it saves every model response, binds and passes tool arguments by name, catches tool exceptions, and displays actual results. Those behaviors differ from the currently downloadable module source. Both versions are preserved; identify which version you are discussing.
