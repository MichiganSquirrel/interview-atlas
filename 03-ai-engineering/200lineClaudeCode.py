# 最小 coding agent：用户提问 → 模型决定是否调用工具 → Python 执行 → 结果回传模型。
# 模型负责生成文字和工具请求；真正读写本地文件的是下面的 Python 函数。

import inspect
import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 把 .env 中的配置加载到环境变量；默认不会覆盖进程中已有的同名变量。
load_dotenv()

# 客户端在各自的调用函数中初始化，因此使用 DeepSeek 时不需要配置 OpenAI Key。
# 在 .env 中自行填写 DEEPSEEK_API_KEY；不要把真实密钥写进代码或提交到 Git。

# System prompt 定义助手行为和文本工具协议，不负责选择模型或设置 API 参数。
# {tool_list_repr} 稍后替换为工具说明；{{JSON_ARGS}} 的双花括号用于转义 str.format。
SYSTEM_PROMPT = """
You are a coding assistant whose goal it is to help us solve coding tasks. 
You have access to a series of tools you can execute. Hear are the tools you can execute:

{tool_list_repr}

When you want to use a tool, reply with exactly one line in the format: 'tool: TOOL_NAME({{JSON_ARGS}})' and nothing else.
Use compact single-line JSON with double quotes. After receiving a tool_result(...) message, continue the task.
If no tool is needed, respond normally.
"""


# ANSI 转义序列：给终端中的用户和助手输出着色，RESET_COLOR 恢复默认颜色。
YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

def resolve_abs_path(path_str: str) -> Path:
    """
    file.py -> /Users/home/mihail/modern-software-dev-lectures/file.py
    """
    # 展开 ~；相对路径基于启动脚本时的工作目录，而非脚本所在目录。
    # 当前没有工作区边界限制，工具可访问进程权限允许的路径。
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path

def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    :param filename: The name of the file to read.
    :return: The full content of the file.
    """
    # 读取整个文件并返回字典；后续会序列化成 JSON，作为模型的上下文。
    full_path = resolve_abs_path(filename)
    print(full_path)
    with open(str(full_path), "r") as f:
        content = f.read()
    return {
        "file_path": str(full_path),
        "content": content
    }

def list_files_tool(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    # 只列当前目录的直接子项，不递归遍历子目录。
    for item in full_path.iterdir():
        all_files.append({
            "filename": item.name,
            "type": "file" if item.is_file() else "dir"
        })
    return {
        "path": str(full_path),
        "files": all_files
    }

def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    :param path: The path to the file to edit.
    :param old_str: The string to replace.
    :param new_str: The string to replace with.
    :return: A dictionary with the path to the file and the action taken.
    """
    full_path = resolve_abs_path(path)
    # 空 old_str 表示写入整个文件：不存在则创建，已存在则覆盖，不会自动创建父目录。
    if old_str == "":
        full_path.write_text(new_str, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "created_file"
        }
    original = full_path.read_text(encoding="utf-8")
    if original.find(old_str) == -1:
        return {
            "path": str(full_path),
            "action": "old_str not found"
        }
    # 最后的 1 表示只替换首次匹配；当前不会检查 old_str 是否有多处匹配。
    edited = original.replace(old_str, new_str, 1)
    full_path.write_text(edited, encoding="utf-8")
    return {
        "path": str(full_path),
        "action": "edited"
    }
    

# 工具注册表：模型输出的工具名 → 本地可调用函数。
# 这里使用自定义文本协议，没有向 API 传入原生 tools / tool_calls。
TOOL_REGISTRY = {
    "read_file": read_file_tool,
    "list_files": list_files_tool,
    "edit_file": edit_file_tool 
}

def get_tool_str_representation(tool_name: str) -> str:
    # __doc__ 读取函数文档；inspect.signature 读取参数签名，一起提供给模型。
    # 因此工具函数的 docstring 也是提示词的一部分。
    tool = TOOL_REGISTRY[tool_name]
    return f"""
    Name: {tool_name}
    Description: {tool.__doc__}
    Signature: {inspect.signature(tool)}
    """

def get_full_system_prompt():
    # 动态拼出所有已注册工具的说明，填入提示词模板。
    tool_str_repr = ""
    for tool_name in TOOL_REGISTRY:
        tool_str_repr += "TOOL\n===" + get_tool_str_representation(tool_name)
        tool_str_repr += f"\n{"="*15}\n"
    return SYSTEM_PROMPT.format(tool_list_repr=tool_str_repr)

def extract_tool_invocations(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Return list of (tool_name, args) requested in 'tool: name({...})' lines.
    The parser expects single-line, compact JSON in parentheses.
    """
    # 例如 tool: read_file({"filename":"main.py"})
    # 会解析成 ("read_file", {"filename": "main.py"})，不会执行任意 Python 表达式。
    invocations = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("tool:"):
            continue
        try:
            after = line[len("tool:"):].strip()
            name, rest = after.split("(", 1)
            name = name.strip()
            if not rest.endswith(")"):
                continue
            json_str = rest[:-1].strip()
            # JSON 文本转换成 Python 对象；当前尚未校验它是否是字典及参数类型。
            args = json.loads(json_str)
            invocations.append((name, args))
        except Exception:
            # 格式错误的工具行会被忽略；若一条也没解析到，外层会当作普通回答。
            continue
    return invocations

def execute_llm_call(conversation: List[Dict[str, str]]):
    # 保留原来的 OpenAI 调用，只有调用本函数时才需要 OPENAI_API_KEY。
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # 每次请求都发送当前 conversation；本脚本不依赖服务端自动保存对话。
    # 未显式传入的参数由 SDK 或服务端采用各自的默认行为。
    response = openai_client.chat.completions.create(
        model="gpt-5",  # 在这里选择模型；使用其他服务时也要改成该服务的模型名。
        messages=conversation,  # 包含角色与内容的消息历史。
        max_completion_tokens=2000  # 生成 token 上限，包含 reasoning tokens，不等于汉字数。
    )
    # 取第一条候选回复的正文；当前没有处理正文为 None 或生成被截断的情况。
    return response.choices[0].message.content

def execute_deepseek_call(conversation: List[Dict[str, str]]):
    """使用 DeepSeek 的 OpenAI 兼容接口，返回回复正文供现有工具解析器处理。"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请先在 .env 中填写 DEEPSEEK_API_KEY=你的DeepSeek密钥")

    # OpenAI 是 SDK 类名；base_url 决定请求实际发送到 DeepSeek。
    with OpenAI(api_key=api_key, base_url="https://api.deepseek.com") as client:
        response = client.chat.completions.create(
            model="deepseek-flash",  # DeepSeek 模型名，不使用 OpenAI 的 gpt-5。
            messages=conversation,
            max_tokens=2000,  # DeepSeek 使用 max_tokens 参数限制生成长度。
            # 先使用非思考模式，直接取得正文并沿用当前的文本工具协议。
            extra_body={"thinking": {"type": "disabled"}},
        )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("DeepSeek 返回了空正文，请检查响应或调整生成上限")
    return content

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
                

# 直接运行此文件时进入交互循环；import 时不会启动循环，
# 但顶层的 .env 加载仍会执行。
if __name__ == "__main__":
    run_coding_agent_loop()
