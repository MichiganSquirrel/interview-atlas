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

下方伪代码和 Python 摘录是本笔记中的改进实现：保存模型消息、按参数名调用工具并捕获工具异常。它与[模块源码](200lineClaudeCode.py)当前的实现存在差异，不能把这些改进视为源码已经具备的行为。

先看伪代码（Pseudocode），把双层循环的骨架和职责理清，再对照下面的完整实现。

```text
初始化：对话历史 = [系统提示词（含工具定义）]

外层循环：等待新的用户任务
    接收用户输入
    如果用户退出：结束外层循环
    将用户任务追加到对话历史

    内层循环：推进当前任务
        发送完整对话历史，请求模型回复
        从回复中解析工具调用列表
        将模型回复追加到对话历史

        如果没有工具调用：
            显示模型回答
            结束内层循环，回到外层等待下一个任务

        对每个工具调用：
            根据工具名从注册表取出函数
            使用参数执行函数，得到结果；执行失败则记录错误
            显示执行结果，并追加到对话历史

        继续内层循环，让模型根据工具结果决定下一步
```

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
        # 当前没有最大步骤数；API 异常仍会向外抛出，工具异常在下方捕获。
        while True:
            assistant_response = execute_llm_call(conversation)
            tool_invocations = extract_tool_invocations(assistant_response)
            # 无论是工具请求还是普通回答，都保存模型消息，保留完整的操作上下文。
            conversation.append({"role": "assistant", "content": assistant_response})
            # 没有识别到工具请求，就展示回答、保存历史，回到外层等待用户输入。
            if not tool_invocations:
                print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {assistant_response}")
                if assistant_response.lstrip().startswith("tool:"):
                    print("[协议错误] 未解析到有效工具调用，上面的文字没有触发文件操作。")
                break
            for name, args in tool_invocations:
                print(name, args)
                try:
                    tool = TOOL_REGISTRY[name]
                    # 按参数名调用；缺少参数直接报错，避免误用默认空串覆盖文件。
                    inspect.signature(tool).bind(**args)
                    resp = tool(**args)
                except (KeyError, TypeError, ValueError, OSError) as exc:
                    resp = {"action": "error", "error": str(exc)}
                # 打印实际返回值：上面的工具名和参数只代表尝试执行，不代表成功。
                print("tool_result:", json.dumps(resp, ensure_ascii=False))
                if name == "edit_file" and resp.get("action") == "old_str not found":
                    print("[编辑失败] old_str 未匹配，文件没有修改；需要重新读取并使用准确原文。")
                # 当前文本协议把工具结果作为 user 消息回传，并非原生 role="tool"。
                # 下一次内层循环会把这些结果发给模型，让它继续决定下一步。
                conversation.append({
                    "role": "user",
                    "content": f"tool_result({json.dumps(resp)})"
                })
```
