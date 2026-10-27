---
title: "The Two Loops of a Coding Agent"
title_en: "The Two Loops of a Coding Agent"
description: "Understand the control flow of a minimal coding agent, from a user task to model requests, tool execution, and returned results."
date: "2026-10-26"
tags: ["interview", "ai-engineering", "agent-loop"]
public: true
source_hash: "2b87019d098ba5edd269c4c88cb5e73cd321093f251829bbd561a166b3ceeee7"
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
        # There is currently no step limit or handling of API/file exceptions here.
        while True:
            assistant_response = execute_llm_call(conversation)
            tool_invocations = extract_tool_invocations(assistant_response)
            # If no tool request is recognized, display the answer, save it in history, and return to user input.
            if not tool_invocations:
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {assistant_response}")
                conversation.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                break
            # The tool branch currently omits assistant_response from history and appends only tool results.
            # The model cannot see its own tool request in later history; this is a possible improvement to the current logic.
            for name, args in tool_invocations:
                # Select functions only from the registry; an unknown tool name raises KeyError.
                tool = TOOL_REGISTRY[name]
                resp = ""
                print(name, args)
                # Read JSON arguments and execute the tool; missing arguments use the defaults shown here.
                if name == "read_file":
                    resp = tool(args.get("filename", "."))
                elif name == "list_files":
                    resp = tool(args.get("path", "."))
                elif name == "edit_file":
                    resp = tool(args.get("path", "."), 
                                args.get("old_str", ""), 
                                args.get("new_str", ""))
                # The current text protocol returns tool results as user messages, rather than native role="tool" messages.
                # The next inner-loop iteration sends these results to the model so it can decide the next step.
                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(resp)})"
                })
```
