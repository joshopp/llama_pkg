from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33
import tool_definitions
import inquirer


setup_prompt_sorting = f"""
You have access to the following functions:

Use the function 'sort_all_bricks' to: Sort all bricks by either color or size. 
{tool_definitions.sort_bricks_definition}


Use the function 'grab_brick' to: Grab and sort one brick specified by its color. 
{tool_definitions.grab_brick}


Use the function 'get_collision_free_bricks' to: Get a list of the size and color of all collision free bricks.
{tool_definitions.get_collision_free_bricks}


Use the function 'get_all_bricks' to: Get a list of all bricks, visible to the robot. Those bricks might not be collision free.
{tool_definitions.get_all_bricks}

Here is an example,
user: How many bricks can you see?
assistant: <tool_call>{{"function_name": "get_all_bricks", "arguments": {{}}}}</tool_call>
ipython: [('4x2', 'orange'), ('4x2', 'green'), ('4x2', 'blue')]
assistant: I can see 1 orange brick with size 4x2, one green brick with size 4x2 and one blue brick with size 4x2.


If a you choose to call a function ONLY reply in the following format:
<tool_call>{{"function_name": function name, "arguments": dictionary of argument name and its value}}</tool_call>
Do not use variables.

Here is an example,
<tool_call>{{"function_name": "sort_all_bricks", "arguments": {{"by_color": true}}}}</tool_call>

Reminder:
- Function calls MUST follow the specified format
- Required parameters MUST be specified
- Put the entire function call reply on one line

You are a helpful assistant. Your name is Panda. 
"""

setup_prompt = f"""You are a helpful assistant. Your name is Panda. You are to answer questions in a scientific way and help the user with their tasks."""


def get_llama_version() -> str:
    questions = [
        inquirer.List('Llama Model',
                      message="What llama model should be used.",
                      choices=['3.1 8B', '3.1 70B', '3.2 1B', '3.3 70B'],
                      carousel=True
                      )
    ]
    result = inquirer.prompt(questions).get("Llama Model", '3.1 8B')
    if result == '3.1 8B':
        return LLAMA_31_8
    elif result == '3.1 70B':
        return LLAMA_31_70
    elif result == '3.2 1B':
        return LLAMA_32
    elif result == '3.3 70B':
        return LLAMA_33


def get_whisper_model() -> str:
    questions = [
        inquirer.List('Whisper Model',
                      message="What whisper model should be used.",
                      choices=['tiny', 'base', 'small', 'medium', 'large-v3'],
                      carousel=True
                      )
    ]
    result = inquirer.prompt(questions).get("Whisper Model", 'medium')
    return result


def get_language() -> str:
    questions = [
        inquirer.List('Language',
                      message="What language should be used.",
                      choices=['en', 'multilingual'],
                      carousel=True
                      )
    ]
    result = inquirer.prompt(questions).get("Language", 'en')
    return "en" if result == "en" else None
