from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33, PandaChatBot
from experiment_prompts_bricks import easy_prompt, easy_target, neutral_prompt, hard_target, hard_prompt
import os
import json
import time

# LList of models
LLAMA_MODELS = [
    (LLAMA_31_8, "3.1 8B"),
    (LLAMA_31_70, "3.1 70B"),
    (LLAMA_32, "3.2 1B"),
    (LLAMA_33, "3.3 70B"),
]

sysprompt_path = '/home/jruopp/Bachelorthesis/src/aria2_ws/Bachelorthesis/data/systemprompts_yuzhi.txt'
with open(sysprompt_path, "r", encoding="utf-8") as file:
    setup_prompt = file.read()


def initialize_bot(llama, llama_version):
    start_time = time.time()
    print(f"Loading Llama version {llama_version}")
    bot = PandaChatBot(llama, setup_prompt)
    init_time = time.time() - start_time
    return bot, init_time


def ask(bot, prompt):
    start_time = time.time()
    bot.clear_history(setup_prompt)
    streamer = bot.generate_chat_response(prompt)
    response = "".join([chunk for chunk in streamer])
    elapsed = time.time() - start_time
    return response, elapsed


def execute_test(bot, prompt, target):
    response, duration = ask(bot, prompt)
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
            if response_json == target_json:
                return "tp", response, duration
            else:
                return "fp", response, duration
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return "fn", response, duration


def test(name, prompts, targets, bot):
    results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    total_time = 0
    texts = []

    for i, prompt in enumerate(prompts):
        res, text, duration = execute_test(bot, prompt, targets[i])
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

    return results, accuracy, precision, avg_time, texts


def aggregate_results(*results_dicts):
    total_results = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for result in results_dicts:
        for key in total_results:
            total_results[key] += result[key]
    return total_results


if __name__ == "__main__":
    benchmark_summary = []

    for llama, llama_version in LLAMA_MODELS:
        # Init bot & measure time
        pandaBot, init_time = initialize_bot(llama, llama_version)
        print("PandaBot initialized")

        # Run tests
        r_easy, acc_easy, prec_easy, time_easy, _ = test("easy", easy_prompt, easy_target, pandaBot)
        r_neut, acc_neut, prec_neut, time_neut, _ = test("neutral", neutral_prompt, [False] * len(neutral_prompt), pandaBot)
        r_hard, acc_hard, prec_hard, time_hard, _ = test("hard", hard_prompt, hard_target, pandaBot)

        total_results = aggregate_results(r_easy, r_neut, r_hard)
        tp = total_results["tp"]
        fp = total_results["fp"]
        tn = total_results["tn"]
        fn = total_results["fn"]
        accuracy = (tp + tn) / max((tp + tn + fp + fn), 1)
        precision = tp / max((tp + fp), 1)

        avg_response_time = (time_easy + time_neut + time_hard) / 3

        # Save results
        file_path = f"llama_experiment/total_result_{llama_version}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(f"Llama Version: {llama_version}\n")
            file.write(f"Initialization Time: {init_time:.2f} sec\n")
            file.write(f"Avg Response Time: {avg_response_time:.2f} sec\n")
            file.write("Test Results Summary:\n")
            for key, value in total_results.items():
                file.write(f"{key}: {value}\n")
            file.write(f"\nAccuracy: {accuracy:.2f}\n")
            file.write(f"Precision: {precision:.2f}\n\n")

        benchmark_summary.append({
            "model": llama_version,
            "init_time_sec": round(init_time, 2),
            "avg_response_time_sec": round(avg_response_time, 2),
            "accuracy": round(accuracy, 2),
            "precision": round(precision, 2)
        })

    # Gesamt-Benchmark speichern
    with open("llama_experiment/benchmark_summary.json", "w") as f:
        json.dump(benchmark_summary, f, indent=2)

    print("Benchmark Summary:")
    print(json.dumps(benchmark_summary, indent=2))
