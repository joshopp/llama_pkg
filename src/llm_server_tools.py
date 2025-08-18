
import inquirer
import zmq

from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_33, LLAMA_32, AriaChatBot
from setup import get_llama_v, setup_prompt_tools

def main():
    print("Running LLama Server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:8001")
    print("ZMQ socket bound to port 8001")

    ariaBot = initialize_bot()
    print("PandaBot initialized")

    while True:
        # Wait for request from Aria PC
        print("Waiting for command from AriaPC...")
        command = socket.recv_string()
        if not command:
            print("No command received, waiting for next message...")
            break
        else:
            print(f"Received command: {command}")

        # generate gpt response
        response = ask(ariaBot, command, setup_prompt_tools)
        print(f"Response: \n {response}\n")

        # send response via 0mq
        socket.send_string(response)
        print("Sent Tool Call provided by Llama in response")
        
        # time.sleep(1)   


def initialize_bot():
    # lama, lama_version = get_llama_v()
    lama, lama_version = LLAMA_31_70, "3.1 70B"
    print(f"Loading Llama version {lama_version}")
    bot = AriaChatBot(lama, setup_prompt_tools)
    return bot
   

def ask(bot, prompt, setup_prompt):
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    # print(f"Prompt:\n{prompt}\nResponse:\n{response}\n")
    return response




if __name__ == "__main__":
    main()