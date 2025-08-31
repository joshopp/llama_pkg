import json
import os
import statistics

from chatbot import LLAMA_31_8, LLAMA_31_70, LLAMA_32, LLAMA_33
from experiment_prompts_toolcall import easy_prompt, easy_target, hard_target, hard_prompt
from llm_utils import initialize_bot, initialize_openai, ask_bot, ask_openai
from setup import setup_prompt_tools


# List of models
LLMs = [
    (LLAMA_31_8, "LLama_3.1_8B"),
    (LLAMA_31_70, "LLama_3.1_70B"),
    (LLAMA_32, "LLama_3.2_1B"),
    (LLAMA_33, "LLama_3.3_70B"),
    ("OpenAI", "GPT-4o"),
]

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# compares result given prompt with target
def execute_test(bot, prompt, target, llama=True):
    if llama:
        response, duration = ask_bot(bot, prompt, setup_prompt_tools)
    else:
        response, duration = ask_openai(bot, prompt, setup_prompt_tools)
    # # print statements to visualize results
    # print(f"response: {response}")
    # print(type(response))
    # print(f"target: {target}")
    # print(type(target))
    # print(response == target)
    if not target:
        if response == "False":
            return "tn", response, duration
        return "fp", response, duration
    else:
        if response == "False":    
            return "fn", response, duration
        try:
            response = json.loads(response)
            if response == target:
                return "tp", response, duration
            return "fn", response, duration
        except Exception as e:
            print(f"Error: {e}")
            return "fn", response, duration


# iterates over all prompts and ouputs results
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

def mean_std(values):
    if len(values) > 1:
        return statistics.mean(values), statistics.stdev(values) 
    else:
        return 0.0, 0.0



def main(iterations, filepath):
    benchmark_summary = []

    for llm, llm_version in LLMs:
        # lists for stats
        accs, precs, init_times, resp_times = [], [], [], []
        accs_easy, precs_easy, times_easy = [], [], []
        accs_hard, precs_hard, times_hard = [], [], []
        total_tp, total_fp, total_tn, total_fn = [], [], [], []
        first_iter_details = None

        # ---------- iterations ----------
        for n in range(iterations):
            # init bot
            if llm == "OpenAI":
                ariaBot, init_time = initialize_openai()
            else:
                ariaBot, init_time = initialize_bot(llm, llm_version, setup_prompt_tools)
            print(f"Iteration {n+1}: AriaBot initialized")

            # run tests
            if llm == "OpenAI":
                r_easy, acc_easy, prec_easy, time_easy, texts_easy = test(
                    easy_prompt, easy_target, ariaBot, llama=False
                )
                r_hard, acc_hard, prec_hard, time_hard, texts_hard = test(
                    hard_prompt, hard_target, ariaBot, llama=False
                )
            else:
                r_easy, acc_easy, prec_easy, time_easy, texts_easy = test(
                    easy_prompt, easy_target, ariaBot
                )
                r_hard, acc_hard, prec_hard, time_hard, texts_hard = test(
                    hard_prompt, hard_target, ariaBot
                )

            # add results
            total_results = aggregate_results(r_easy, r_hard)
            tp = total_results["tp"]
            fp = total_results["fp"]
            tn = total_results["tn"]
            fn = total_results["fn"]

            accuracy = (tp + tn) / max((tp + tn + fp + fn), 1)
            precision = tp / max((tp + fp), 1)
            avg_response_time = (time_easy + time_hard) / 2

            # collect results
            accs.append(accuracy)
            precs.append(precision)
            init_times.append(init_time)
            resp_times.append(avg_response_time)
            total_tp.append(tp)
            total_fp.append(fp)
            total_tn.append(tn)
            total_fn.append(fn)

            accs_easy.append(acc_easy)
            precs_easy.append(prec_easy)
            times_easy.append(time_easy)

            accs_hard.append(acc_hard)
            precs_hard.append(prec_hard)
            times_hard.append(time_hard)

            # long output for first iteration
            if n == 0:
                first_iter_details = {
                    "init_time": init_time,
                    "avg_response_time": avg_response_time,
                    "accuracy": accuracy,
                    "precision": precision,
                    "tp": tp, "fp": fp, "tn": tn, "fn": fn,
                    "acc_easy": acc_easy, "prec_easy": prec_easy, "time_easy": time_easy, "texts_easy": texts_easy,
                    "acc_hard": acc_hard, "prec_hard": prec_hard, "time_hard": time_hard, "texts_hard": texts_hard,
                }

        # ---------- aggregation ----------
        mean_acc, std_acc = mean_std(accs)
        mean_prec, std_prec = mean_std(precs)
        mean_init, std_init = mean_std(init_times)
        mean_resp, std_resp = mean_std(resp_times)

        mean_acc_easy, std_acc_easy = mean_std(accs_easy)
        mean_prec_easy, std_prec_easy = mean_std(precs_easy)
        mean_time_easy, std_time_easy = mean_std(times_easy)

        mean_acc_hard, std_acc_hard = mean_std(accs_hard)
        mean_prec_hard, std_prec_hard = mean_std(precs_hard)
        mean_time_hard, std_time_hard = mean_std(times_hard)

        mean_tp, mean_fp = statistics.mean(total_tp), statistics.mean(total_fp)
        mean_tn, mean_fn = statistics.mean(total_tn), statistics.mean(total_fn)

        # ---------- Save results ----------
        file_path = os.path.join(filepath, f"total_result_{llm_version}_1")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(f"LLM Version: {llm_version}\n\n")

            file.write("=== Global statistics (10 iterations) ===\n")
            file.write(f"Initialization Time: {mean_init:.2f} ± {std_init:.2f} sec\n")
            file.write(f"Response Time: {mean_resp:.2f} ± {std_resp:.2f} sec\n")
            file.write(f"Accuracy: {mean_acc:.2f} ± {std_acc:.2f}\n")
            file.write(f"Precision: {mean_prec:.2f} ± {std_prec:.2f}\n\n")

            file.write("=== Confusion matrix (mean counts) ===\n")
            file.write(f"TP={mean_tp:.1f}, FP={mean_fp:.1f}, TN={mean_tn:.1f}, FN={mean_fn:.1f}\n\n")

            file.write("=== Easy set statistics ===\n")
            file.write(f"Accuracy: {mean_acc_easy:.2f} ± {std_acc_easy:.2f}\n")
            file.write(f"Precision: {mean_prec_easy:.2f} ± {std_prec_easy:.2f}\n")
            file.write(f"Response Time: {mean_time_easy:.2f} ± {std_time_easy:.2f} sec\n\n")

            file.write("=== Hard set statistics ===\n")
            file.write(f"Accuracy: {mean_acc_hard:.2f} ± {std_acc_hard:.2f}\n")
            file.write(f"Precision: {mean_prec_hard:.2f} ± {std_prec_hard:.2f}\n")
            file.write(f"Response Time: {mean_time_hard:.2f} ± {std_time_hard:.2f} sec\n\n")

            file.write("=== First iteration detailed results ===\n")
            file.write(f"Initialization Time: {first_iter_details['init_time']:.2f} sec\n")
            file.write(f"Response Time: {first_iter_details['avg_response_time']:.2f} sec\n")
            file.write(f"Accuracy: {first_iter_details['accuracy']:.2f}\n")
            file.write(f"Precision: {first_iter_details['precision']:.2f}\n")
            file.write(f"TP={first_iter_details['tp']}, FP={first_iter_details['fp']}, "
                       f"TN={first_iter_details['tn']}, FN={first_iter_details['fn']}\n\n")

            file.write("--- Easy Test Results ---\n")
            file.write(f"Accuracy: {first_iter_details['acc_easy']:.2f}\n")
            file.write(f"Precision: {first_iter_details['prec_easy']:.2f}\n")
            file.write(f"Avg Time: {first_iter_details['time_easy']:.2f} sec\n")
            for text in first_iter_details["texts_easy"]:
                file.write(text + "\n")

            file.write("\n--- Hard Test Results ---\n")
            file.write(f"Accuracy: {first_iter_details['acc_hard']:.2f}\n")
            file.write(f"Precision: {first_iter_details['prec_hard']:.2f}\n")
            file.write(f"Avg Time: {first_iter_details['time_hard']:.2f} sec\n")
            for text in first_iter_details["texts_hard"]:
                file.write(text + "\n")

        benchmark_summary.append({
            "model": llm_version,
            "init_time_mean_sec": round(mean_init, 2),
            "init_time_std_sec": round(std_init, 2),
            "avg_response_time_mean_sec": round(mean_resp, 2),
            "avg_response_time_std_sec": round(std_resp, 2),
            "accuracy_mean": round(mean_acc, 2),
            "accuracy_std": round(std_acc, 2),
            "precision_mean": round(mean_prec, 2),
            "precision_std": round(std_prec, 2),
        })

        print(f"{llm_version}: finished")



if __name__ == "__main__":
    file_path = f"/home/jruopp/thesis_ws/src/llama_pkg/data/llama_experiment/intent"
    iterations = 10
    main()