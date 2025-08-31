import inquirer
from openai import OpenAI
import time
from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33, AriaChatBot

def initialize_bot(llama, llama_version, setup_prompt):
    start_time = time.time()
    print(f"Loading Llama version {llama_version}")
    bot = AriaChatBot(llama, setup_prompt)
    init_time = time.time() - start_time
    return bot, init_time

def initialize_openai():
    start_time = time.time()
    print(f"Loading OpenAI client")
    # use custom API key
    api_key = ""
    client = OpenAI(api_key=api_key)
    init_time = time.time() - start_time
    return client, init_time

def ask_bot(bot, prompt, setup_prompt):
    start_time = time.time()
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    elapsed = time.time() - start_time
    return response, elapsed

def ask_openai(client, prompt, setup_prompt):
    messages = []
    messages.append({"role": "system", "content": setup_prompt})
    messages.append({"role": "user", "content": prompt})

    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    elapsed = time.time() - start_time
    return response.choices[0].message.content, elapsed

def get_llama_v() -> str:
    questions = [
        inquirer.List('Llama Model',
                      message="What llama model should be used.",
                      choices=['3.1 8B', '3.1 70B', '3.2 1B', '3.3 70B'],
                      carousel=True
                      )
    ]
    result = inquirer.prompt(questions).get("Llama Model", '3.1 8B')
    if result == '3.1 8B':
        return LLAMA_31_8, '3.1 8B'
    elif result == '3.1 70B':
        return LLAMA_31_70, '3.1 70B'
    elif result == '3.2 1B':
        return LLAMA_32, '3.2 1B'
    elif result == '3.3 70B':
        return LLAMA_33, '3.3 70B'