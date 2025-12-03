import time
import os
import subprocess
from llama_cpp import Llama

MODEL_PATH = "./mistral-7b-instruct-v0.2.Q4_K_M.gguf"

def clear_cache():
    # This command forces Linux to drop cached files from RAM
    print(" [System] Clearing OS Page Cache...")
    subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"])

def benchmark_load(label):
    start = time.time()
    # n_gpu_layers=0 forces CPU
    llm = Llama(model_path=MODEL_PATH, n_threads=4, verbose=False)
    duration = time.time() - start
    print(f" {label} Load Time: {duration:.4f} seconds")

print("--- STARTING SYSTEM MEMORY TEST ---")

# TEST 1: COLD START (Simulating a fresh server boot)
clear_cache()
benchmark_load("COLD START (Disk Read)")

# TEST 2: WARM START (Simulating subsequent requests)
# We do NOT clear cache here. Linux keeps the file in RAM.
benchmark_load("WARM START (RAM Cache)")

print("---------------------------------------")
