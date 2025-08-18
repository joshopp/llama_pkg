from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33, PandaChatBot, AriaChatBot
from experiment_prompts_functions import easy_prompt, easy_target, neutral_prompt, hard_target, hard_prompt
from setup import setup_prompt
from tool_utils import parse_tools
import inquirer
import os


def execute_test(prompt, target):
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    tools = parse_tools(response)
    if not tools and not target:
        return "tn", response
    elif not tools and target:
        return "fn", response
    elif tools and not target:
        return "fp", response
    elif tools and target:
        if tools[0] == target or tools == target:
            return "tp", response
        else:
            return "fn", response


def execute_test_user_input(prompt, target):
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    print(f"Prompt:\n{prompt}\nResponse:\n{response}\nTarget:\n{target}\n\n")
    questions = [
        inquirer.List('result',
                      message="Choose",
                      choices=['tp', 'fp', "tn", "fn"],
                      carousel=True
                      )
    ]
    result = inquirer.prompt(questions).get('result')
    return result, response


def test(name, prompts, target, with_user=False):
    results = {"tp": 0, "fp": 0,
               "tn": 0, "fn": 0}
    texts = []
    for i, prompt in enumerate(prompts):
        result, text = execute_test_user_input(
            prompt, target[i]) if with_user else execute_test(prompt, target[i])
        results[result] += 1
        texts.append(
            f"Prompt {i + 1}:\n{prompt}\nResponse:\n{text}\Result:\n{result}\n\n")
    tp = results["tp"]
    fp = results["fp"]
    tn = results["tn"]
    fn = results["fn"]

    accuracy = (tp + tn) / (tp + tn + fp +
                            fn) if (tp + tn + fp + fn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    file_path = "llama_experiment/" + name + "_" + lama_version
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write("Test Results Summary:\n")
        for key, value in results.items():
            file.write(f"{key}: {value}\n")
        file.write(f"\nAccuracy: {accuracy:.2f}\n")
        file.write(f"Precision: {precision:.2f}\n\n")
        file.write("\nDetailed Responses:\n")
        file.writelines(texts)
    print(f"{name}: {results}, acuraccy: {accuracy}")
    return results


def aggregate_results(*results_dicts):
    total_results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for result in results_dicts:
        for key in total_results:
            total_results[key] += result[key]
    return total_results

def execute_question(prompt):
    print("Starting Llama tests...")
    lama, lama_version = get_llama_v()
    bot = AriaChatBot(lama, setup_prompt)

    bot.clear_history(setup_prompt)

    # prompt = "What is the capital of France?"
    streamer = bot.generate_chat_response(prompt)
    print(f"Prompt:\n{prompt}\nResponse:\n", end="", flush=True)
    for chunk in streamer:
        print(chunk, end="", flush=True)
    print()  # for newline after the response

if __name__ == "__main__":
    lama, lama_version = get_llama_v()
    bot = PandaChatBot(lama, setup_prompt=setup_prompt)
    r_1 = test("easy", easy_prompt, easy_target)
    r_2 = test("neutral", neutral_prompt, [False] * 12)
    r_3 = test("hard", hard_prompt, hard_target, with_user=True)

    total_results = aggregate_results(r_1, r_2, r_3)

    tp = total_results["tp"]
    fp = total_results["fp"]
    tn = total_results["tn"]
    fn = total_results["fn"]
    accuracy = (tp + tn) / (tp + tn + fp +
                            fn) if (tp + tn + fp + fn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0

    with open("llama_experiment/" + "total_result" + lama_version, "w") as file:
        file.write("Test Results Summary:\n")
        for key, value in total_results.items():
            file.write(f"{key}: {value}\n")
        file.write(f"\nAccuracy: {accuracy:.2f}\n")
        file.write(f"Precision: {precision:.2f}\n\n")
