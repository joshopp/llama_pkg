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