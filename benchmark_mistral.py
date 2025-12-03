import time
import psutil
import json
from llama_cpp import Llama

# CONFIGURATION
MODEL_PATH = "./mistral-7b-instruct-v0.2.Q4_K_M.gguf"
THREAD_COUNTS = [1, 2, 4] # We test scaling across your 4 vCPUs
PROMPT = "Q: Write a short poem about the rust programming language. A: "
RESULTS = []

def get_ram_usage():
    # Returns RAM usage in GB
    return psutil.Process().memory_info().rss / (1024 ** 3)

print(f"{'Threads':<10} | {'Load Time (s)':<15} | {'Speed (t/s)':<15} | {'RAM (GB)':<10}")
print("-" * 60)

for n_threads in THREAD_COUNTS:
    # 1. Measure Load Time (Cold Start simulation)
    # We reload the model every time to ensure isolation
    start_load = time.time()
    llm = Llama(
        model_path=MODEL_PATH,
        n_threads=n_threads,
        n_ctx=2048,
        verbose=False
    )
    load_time = time.time() - start_load

    # 2. Warmup (Process one token to initialize caches)
    llm("Test", max_tokens=1)
    
    # 3. Measure Inference Speed
    start_gen = time.time()
    output = llm(PROMPT, max_tokens=100, stop=["Q:", "\n"])
    end_gen = time.time()
    
    token_count = output['usage']['completion_tokens']
    duration = end_gen - start_gen
    speed = token_count / duration
    ram_gb = get_ram_usage()

    # 4. Log and Print
    result = {
        "threads": n_threads,
        "load_time_sec": round(load_time, 2),
        "speed_tps": round(speed, 2),
        "ram_gb": round(ram_gb, 2)
    }
    RESULTS.append(result)
    
    print(f"{n_threads:<10} | {load_time:<15.2f} | {speed:<15.2f} | {ram_gb:<10.2f}")

# Save detailed results for your GitHub
with open("benchmark_results.json", "w") as f:
    json.dump(RESULTS, f, indent=4)

print("\nBenchmark complete. Results saved to benchmark_results.json")
