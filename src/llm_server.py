import zmq

from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_33, LLAMA_32, AriaChatBot
from llm_utils import initialize_bot, ask_bot
from setup import setup_prompt_tools, setup_prompt_intention, get_llama_v

def main():
    print("Running LLama Server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:8000")
    print("ZMQ socket bound to port 8000")

    # initialize Llama
    llama, llama_version = get_llama_v()
    # llama, llama_version = LLAMA_33, "3.3 70B"
    ariaBot, _ = initialize_bot(llama, llama_version, "")
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
        response_tool, _ = ask_bot(ariaBot, command, setup_prompt_tools)
        print(f"Tool Response: \n {response_tool}\n")

        response_intent, _ = ask_bot(ariaBot, command, setup_prompt_intention)
        print(f"Intent Response: \n {response_intent}\n")

        # send response via 0mq
        response = {
            "tool": response_tool,
            "intent": response_intent
        }
        socket.send_json(response)
        print("Sent Response provided by Llama in response")


if __name__ == "__main__":
    main()