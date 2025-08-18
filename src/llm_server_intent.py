
import inquirer
import time
import zmq
from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_33, LLAMA_32, PandaChatBot

def main():
    print("Running LLama Server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:8000")
    print("ZMQ socket bound to port 8000")

    pandaBot, setup_prompt = initialize_bot()
    print("PandaBot initialized")

    while True:
        # Wait for request from Aria PC
        print("Waiting for question from Aria PC...")
        question = socket.recv_string()
        if not question:
            print("No question received, waiting for next message...")
            break
        else:
            print(f"Received question: {question}")

        # generate gpt response
        response = ask(pandaBot, question, setup_prompt)
        print(f"Response: \n {response}\n")    

        # send response via 0mq
        socket.send_string(response)
        print("Sent LLama answer in response")
        
        # time.sleep(1)   


def initialize_bot():
    sysprompt_path = '/home/jruopp/thesis_ws/src/llama_pkg/data/systemprompts_brick.txt'
    with open(sysprompt_path, "r", encoding="utf-8") as file:
        setup_prompt = file.read()

    # lama, lama_version = get_llama_v()
    lama, lama_version = LLAMA_31_70, "3.1 70B"
    print(f"Loading Llama version {lama_version}")
    bot = PandaChatBot(lama, setup_prompt)

    return bot, setup_prompt
   

def ask(bot, prompt, setup_prompt):
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    # print(f"Prompt:\n{prompt}\nResponse:\n{response}\n")
    return response



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




if __name__ == "__main__":
    main()