import json
import re


def convert_tool_call_into_chat_message(text):
    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    tool_call_match = re.findall(tool_call_pattern, text, re.DOTALL)
    tool_calls = [json.loads(match.strip()) for match in tool_call_match]
    return [{"type": "function", "function": tool_call} for tool_call in tool_calls]


def check_if_tool_call(chunk):
    return chunk.startswith("<tool_call>")


def parse_tools(tools):
    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    tool_call_match = re.findall(tool_call_pattern, tools, re.DOTALL)
    tool_calls = [convert_recursively(match.strip())
                  for match in tool_call_match]
    return tool_calls


def convert_recursively(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_recursively(value)
    elif isinstance(data, list):
        data = [convert_recursively(item) for item in data]
    return data


def extract_python_code(content):
    if content == "False": return False

    code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)
        if full_code.startswith("json"):
            full_code = full_code[5:]
        return full_code
    else:
        return content
    
def compare_json(response, target):
    if response.keys() != target.keys():
        return False
    if set(response["object_name"]) != set(target["object_name"]):
        return False
    return True