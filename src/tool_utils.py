import json
import re


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