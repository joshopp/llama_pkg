import json
from openai import OpenAI
import os
import time

from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33, AriaChatBot
from experiment_prompts_JSON import easy_prompt, easy_target, neutral_prompt, hard_target, hard_prompt
from setup import setup_prompt_intention
from tool_utils import compare_json, extract_python_code

# List of models
LLMs = [
    (LLAMA_31_8, "LLama_3.1_8B"),
    (LLAMA_31_70, "LLama_3.1_70B"),
    (LLAMA_32, "LLama_3.2_1B"),
    (LLAMA_33, "LLama_3.3_70B"),
    ("OpenAI", "GPT-4o"),
]

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def initialize_bot(llama, llama_version):
    start_time = time.time()
    print(f"Loading Llama version {llama_version}")
    bot = AriaChatBot(llama, setup_prompt_intention)
    init_time = time.time() - start_time
    return bot, init_time


def ask(bot, prompt):
    start_time = time.time()
    bot.clear_history(setup_prompt_intention)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    elapsed = time.time() - start_time
    return response, elapsed


def execute_test(bot, prompt, target, llama=True):
    if llama:
        response, duration = ask(bot, prompt)
    else:
        response, duration = ask_openai(bot, prompt)
    response = extract_python_code(response)

    if not response and not target:
        return "tn", response, duration
    elif not response and target:
        return "fn", response, duration
    elif response and not target:
        return "fp", response, duration
    elif response and target:
        try:
            response_json = json.loads(response)
            target_json = json.loads(target)
            response_str = json.dumps(response_json, ensure_ascii=False, separators=(',', ':'))
            target_str = json.dumps(target_json, ensure_ascii=False, separators=(',', ':'))
            if response_str == target_str:
                return "tp", response, duration
            else:
                return "fp", response, duration
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return "fn", response, duration


def test(prompts, targets, bot, llama = True):
    results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    total_time = 0
    texts = []

    for i, prompt in enumerate(prompts):
        res, text, duration = execute_test(bot, prompt, targets[i], llama)
        results[res] += 1
        total_time += duration
        texts.append(
            f"Prompt {i + 1}:\n{prompt}\nResponse:\n{text}\nResult:\n{res}\n\n"
        )

    tp = results["tp"]
    fp = results["fp"]
    tn = results["tn"]
    fn = results["fn"]

    accuracy = (tp + tn) / max((tp + tn + fp + fn), 1)
    precision = tp / max((tp + fp), 1)
    avg_time = total_time / len(prompts) if prompts else 0
    print("test finished")
    return results, accuracy, precision, avg_time, texts


def aggregate_results(*results_dicts):
    total_results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for result in results_dicts:
        for key in total_results:
            total_results[key] += result[key]
    return total_results


def initialize_openai():
    start_time = time.time()
    print(f"Loading OpenAI client")
    api_key = "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"
    client = OpenAI(api_key=api_key)
    init_time = time.time() - start_time
    return client, init_time


def ask_openai(client, prompt):
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    elapsed = time.time() - start_time
    return response.choices[0].message.content, elapsed




if __name__ == "__main__":
    benchmark_summary = []

    for llm, llm_version in LLMs:
        # Init bot & measure time
        if llm == "OpenAI":
            ariaBot, init_time = initialize_openai()
        else:
            ariaBot, init_time = initialize_bot(llm, llm_version)
        print("AriaBot initialized")

        # Run tests
        if llm == "OpenAI":
            r_easy, acc_easy, prec_easy, time_easy, texts_easy = test(easy_prompt, easy_target, ariaBot, llama=False)
            r_neut, acc_neut, prec_neut, time_neut, texts_neut = test(neutral_prompt, [False] * len(neutral_prompt), ariaBot, llama=False)
            r_hard, acc_hard, prec_hard, time_hard, texts_hard = test(hard_prompt, hard_target, ariaBot, llama=False)
        else:
            r_easy, acc_easy, prec_easy, time_easy, texts_easy = test(easy_prompt, easy_target, ariaBot)
            r_neut, acc_neut, prec_neut, time_neut, texts_neut = test(neutral_prompt, [False] * len(neutral_prompt), ariaBot)
            r_hard, acc_hard, prec_hard, time_hard, texts_hard = test(hard_prompt, hard_target, ariaBot)

        total_results = aggregate_results(r_easy, r_neut, r_hard)
        tp = total_results["tp"]
        fp = total_results["fp"]
        tn = total_results["tn"]
        fn = total_results["fn"]
        accuracy = (tp + tn) / max((tp + tn + fp + fn), 1)
        precision = tp / max((tp + fp), 1)

        avg_response_time = (time_easy + time_neut + time_hard) / 3

        # Save results
        file_path = f"/home/jruopp/thesis_ws/src/llama_pkg/data/llama_experiment/total_result_{llm_version}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(f"LLM Version: {llm_version}\n")
            file.write(f"Initialization Time: {init_time:.2f} sec\n")
            file.write(f"Avg Response Time: {avg_response_time:.2f} sec\n")
            file.write("Test Results Summary:\n")
            for key, value in total_results.items():
                file.write(f"{key}: {value}\n")
            file.write(f"\nAccuracy: {accuracy:.2f}\n")
            file.write(f"Precision: {precision:.2f}\n\n")

            # Save detailed results for each test
            file.write("\n--- Easy Test Results ---\n")
            file.write(f"Accuracy: {acc_easy:.2f}\n")
            file.write(f"Precision: {prec_easy:.2f}\n")
            file.write(f"Avg Time: {time_easy:.2f} sec\n")
            for text in texts_easy:
                file.write(text + "\n")
            file.write("\n--- Neutral Test Results ---\n")
            file.write(f"Accuracy: {acc_neut:.2f}\n")
            file.write(f"Precision: {prec_neut:.2f}\n")
            file.write(f"Avg Time: {time_neut:.2f} sec\n")
            for text in texts_neut:
                file.write(text + "\n")
            file.write("\n--- Hard Test Results ---\n")
            file.write(f"Accuracy: {acc_hard:.2f}\n")
            file.write(f"Precision: {prec_hard:.2f}\n")
            file.write(f"Avg Time: {time_hard:.2f} sec\n")
            for text in texts_hard:
                file.write(text + "\n")

        benchmark_summary.append({
            "model": llm_version,
            "init_time_sec": round(init_time, 2),
            "avg_response_time_sec": round(avg_response_time, 2),
            "accuracy": round(accuracy, 2),
            "precision": round(precision, 2)
        })
        print(f"{llm_version}: finished")

