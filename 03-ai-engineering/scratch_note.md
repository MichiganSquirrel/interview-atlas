---
title: "Coding Agent 的双层循环"
title_en: "The Two Loops of a Coding Agent"
description: "从用户任务、模型请求、工具执行到结果回传，理解最小 Coding Agent 的控制流程。"
date: "2026-10-26"
tags: ["interview", "ai-engineering", "agent-loop"]
public: true
---

# Coding Agent 的双层循环

to model：这里加上原本的代码和注释

下面的流程图保留了这篇笔记的核心：外层循环（Outer Loop）接收新的用户任务，内层循环（Inner Loop）推进当前任务。理解这个划分，可以把模型生成、工具执行和对话历史三个职责连起来。

```text
coding agent的核心：
外层循环：等待用户输入一个任务
    ↓
内层循环：请求模型 → 执行工具 → 把结果交回模型
    ↑                         ↓
    └──── 模型还要用工具 ──────┘
                              ↓
                         模型直接回答
                              ↓
                        回到外层等待输入
```

## 代码与注释

```python
def run_coding_agent_loop():
    # 启动时打印完整提示词，便于观察模型看到的工具定义。
    print(get_full_system_prompt())
    # conversation 是保存在内存里的对话历史，退出后不会持久化。
    conversation = [{
        "role": "system",
        "content": get_full_system_prompt()
    }]
    # 外层循环：接收用户的新任务。
    while True:
        try:
            user_input = input(f"{YOU_COLOR}You:{RESET_COLOR}:")
        # 在等待输入时，Ctrl+C 或输入结束可退出。
        except (KeyboardInterrupt, EOFError):
            break
        conversation.append({
            "role": "user",
            "content": user_input.strip()
        })
        # 内层 agent loop：同一个任务可以连续调用多次工具，再给出普通回答。
        # 当前没有最大步骤数，也没有在这里捕获 API / 文件操作异常。
        while True:
            # 如需切回 OpenAI，启用下一行，并注释 DeepSeek 调用。
            # assistant_response = execute_llm_call(conversation)
            assistant_response = execute_deepseek_call(conversation)
            tool_invocations = extract_tool_invocations(assistant_response)
            # 没有识别到工具请求，就展示回答、保存历史，回到外层等待用户输入。
            if not tool_invocations:
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {assistant_response}")
                conversation.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                break
            # 注意：当前工具分支未将 assistant_response 加入历史，只追加工具结果。
            # 后续模型因此看不到自己发出的这条工具请求；这是现有逻辑的一个待改进点。
            for name, args in tool_invocations:
                # 只从注册表选函数；未知工具名会触发 KeyError。
                tool = TOOL_REGISTRY[name]
                resp = ""
                print(name, args)
                # 从 JSON 参数中取值并执行工具；缺失参数采用这里给出的默认值。
                if name == "read_file":
                    resp = tool(args.get("filename", "."))
                elif name == "list_files":
                    resp = tool(args.get("path", "."))
                elif name == "edit_file":
                    resp = tool(args.get("path", "."), 
                                args.get("old_str", ""), 
                                args.get("new_str", ""))
                # 当前文本协议把工具结果作为 user 消息回传，并非原生 role="tool"。
                # 下一次内层循环会把这些结果发给模型，让它继续决定下一步。
                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(resp)})"
                })
```
