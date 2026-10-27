---
title: "The Two Loops of a Coding Agent"
title_en: "The Two Loops of a Coding Agent"
description: "Understand the control flow of a minimal coding agent, from a user task to model requests, tool execution, and returned results."
date: "2026-10-26"
tags: ["interview", "ai-engineering", "agent-loop"]
public: true
source_hash: "5d60353ff65b96f717f61a6c1e312655d9f8a37700ed2216bae34b5c787cfd0c"
---

# The Two Loops of a Coding Agent

The diagram preserves the central idea of the original note: the outer loop accepts a new user task, while the inner loop advances the current task. This distinction connects three responsibilities: model generation, tool execution, and conversation history.

```text
The core of a coding agent:
Outer loop: wait for a user task
    ↓
Inner loop: request model → execute tool → return result to model
    ↑                                           ↓
    └────────── model needs another tool ────────┘
                                                ↓
                                      model answers directly
                                                ↓
                                      return to user input
```

## Outer loop: accept a task and retain context

In [the Python example in this module](200lineClaudeCode.py), `run_coding_agent_loop()` creates `conversation` before entering the outer `while True` loop that waits for user input. The input is appended as a `user` message, and control moves into the inner loop. Once the model finishes an answer, the program returns to the input prompt and waits for another question.

A new task does not clear the history here. Because `conversation` is created before the outer loop, later inputs retain earlier messages. This provides context for follow-ups such as “continue editing that file.” History lives in memory; the current script does not persist the conversation after exit.

## Inner loop: the model chooses the next step and Python executes tools

The inner loop first calls `execute_llm_call(conversation)`. The model's text is parsed by `extract_tool_invocations()`. If it yields a single-line request such as `tool: read_file({"filename":"main.py"})`, the program selects the corresponding function from the tool registry and executes it. The model generates a tool name and arguments; a local Python function performs the actual file read or edit.

The result is serialized as `tool_result(...)` and appended to the message history. The next iteration sends it back to the model along with the history. A single task can therefore read a file, edit it, and finally produce an explanation. A tool call does not end the task; it supplies information needed for the next decision.

This example uses a custom text protocol: results are returned as `user` messages, and the code does not pass the API's native `tools` or `tool_calls`. Explain this convention when describing the implementation. A function name appearing in model output does not itself execute a local function.

## Follow one file edit through both loops

Suppose the user enters “Inspect `main.py` and change the greeting to Hello.” The outer loop accepts the input and enters the inner loop. The first model response might request `read_file`, after which the program reads and returns the content. The second response might request `edit_file` based on that content; the program replaces the first matching occurrence and returns the result. A third response gives an ordinary explanation, ending the inner loop. The outer loop then waits for another user input.

This is a possible trace for explaining control flow, not the result of an experiment that was actually run. The model may produce different output, and the example's parser may ignore malformed tool requests.

## Termination and the boundaries of the current implementation

When no tool request is parsed, the current code displays the response as an ordinary answer and exits the inner loop. “No tool request” is therefore the implemented termination condition; it does not itself prove that the task was completed correctly. A malformed tool request can reach the same branch.

The tool branch currently appends only the execution result and omits the model's tool request, leaving that request absent from later history. The inner loop also has no maximum step count or shared exception handling. These are behaviors to identify when reading the existing implementation; the source code remains unchanged. The outer loop exits when Ctrl+C or end-of-input (EOF) occurs while waiting for input.

[Return to AI-assisted Software Engineering](README.md)
