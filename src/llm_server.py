import zmq

from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_33, LLAMA_32, AriaChatBot
from setup import setup_prompt_tools, setup_prompt_intention

def main():
    print("Running LLama Server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:8000")
    print("ZMQ socket bound to port 8000")

    ariaBot = initialize_bot()
    print("AriaBot initialized")

    while True:
        # Wait for request from Aria PC
        print("Waiting for command from AriaPC...")
        command = socket.recv_string()
        if not command:
            print("No command received, waiting for next message...")
            break
        else:
            print(f"Received command: {command}")

        # generate gpt responses (tool + intent)
        response_tool = ask(ariaBot, command, setup_prompt_tools)
        print(f"Tool Response: \n {response_tool}\n")

        response_intent = ask(ariaBot, command, setup_prompt_intention)
        print(f"Intent Response: \n {response_intent}\n")

        # send response via 0mq
        response = {
            "tool": response_tool,
            "intent": response_intent
        }
        socket.send_json(response)
        print("Sent Response provided by Llama in response")

        # time.sleep(1)   


def initialize_bot():
    # lama, lama_version = get_llama_v()
    lama, lama_version = LLAMA_33, "3.3 70B"
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