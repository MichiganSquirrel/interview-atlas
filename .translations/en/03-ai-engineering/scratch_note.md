---
title: "The Two Loops of a Coding Agent"
title_en: "The Two Loops of a Coding Agent"
description: "Understand the control flow of a minimal coding agent, from a user task to model requests, tool execution, and returned results."
date: "2026-10-26"
tags: ["interview", "ai-engineering", "agent-loop"]
public: true
source_hash: "58a1b88abf2d2ebcb338a889c03738cfafad342bfc1318cdd99b6e15d1ed1272"
---

# The Two Loops of a Coding Agent

to model: add the original code and comments here

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

## Code and comments

Read the pseudocode first to understand the two loops and their responsibilities, then compare it with the full implementation below.

```text
Initialize: conversation history = [system prompt, including tool definitions]

Outer loop: wait for a new user task
    Receive user input
    If the user exits: end the outer loop
    Append the user task to the conversation history

    Inner loop: advance the current task
        Send the full conversation history and request a model reply
        Parse the reply for tool calls
        Append the model reply to the conversation history

        If there are no tool calls:
            Display the model answer
            End the inner loop and wait for the next task in the outer loop

        For each tool call:
            Look up the function by tool name in the registry
            Execute it with the arguments; record any execution error
            Display the result and append it to the conversation history

        Continue the inner loop so the model can decide what to do next
```

```python
def run_coding_agent_loop():
    # Print the full prompt at startup to inspect the tool definitions seen by the model.
    print(get_full_system_prompt())
    # conversation is in-memory message history and is not persisted after exit.
    conversation = [{
        "role": "system",
        "content": get_full_system_prompt()
    }]
    # Outer loop: accept a new user task.
    while True:
        try:
            user_input = input(f"{YOU_COLOR}You:{RESET_COLOR}:")
        # While waiting for input, Ctrl+C or end-of-input exits the loop.
        except (KeyboardInterrupt, EOFError):
            break
        conversation.append({
            "role": "user",
            "content": user_input.strip()
        })
        # Inner agent loop: a task can call tools repeatedly before producing an ordinary answer.
        # There is no step limit; API exceptions propagate, while tool exceptions are caught below.
        while True:
            assistant_response = execute_llm_call(conversation)
            tool_invocations = extract_tool_invocations(assistant_response)
            # Save model messages for both tool requests and ordinary replies to preserve the operation history.
            conversation.append({"role": "assistant", "content": assistant_response})
            # If no tool request is recognized, display the answer and return to the outer input loop.
            if not tool_invocations:
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {assistant_response}")
                if assistant_response.lstrip().startswith("tool:"):
                    print("[协议错误] 未解析到有效工具调用，上面的文字没有触发文件操作。")
                break
            for name, args in tool_invocations:
                print(name, args)
                try:
                    tool = TOOL_REGISTRY[name]
                    # Call by parameter name; missing arguments raise errors rather than defaulting to empty strings that overwrite files.
                    inspect.signature(tool).bind(**args)
                    resp = tool(**args)
                except (KeyError, TypeError, ValueError, OSError) as exc:
                    resp = {"action": "error", "error": str(exc)}
                # Print the actual result: the tool name and arguments above indicate an attempt, not success.
                print("tool_result:", json.dumps(resp, ensure_ascii=False))
                if name == "edit_file" and resp.get("action") == "old_str not found":
                    print("[编辑失败] old_str 未匹配，文件没有修改；需要重新读取并使用准确原文。")
                # This text protocol returns tool results as user messages, rather than native role="tool" messages.
                # The next inner-loop iteration sends these results to the model so it can decide the next step.
                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(resp)})"
                })
```
