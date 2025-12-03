import time
import psutil
import os
import gc
from llama_cpp import Llama

# CONFIGURATION
PROMPT_MISTRAL = "Q: Write a short poem about the rust programming language. A: "
PROMPT_PHI3 = "<|user|>\nWrite a short poem about the rust programming language.<|end|>\n<|assistant|>"

MODELS = [
    {
        "name": "Mistral-7B (Baseline)",
        "path": "./mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "threads": [2, 4], 
        "n_ctx": 2048,
        "prompt": PROMPT_MISTRAL,
        "stop": ["Q:", "\n"]
    },
    {
        "name": "Phi-3-Mini (Optimized)",
        "path": "./Phi-3-mini-4k-instruct-q4.gguf",
        "threads": [4],
        "n_ctx": 4096, # Native context for Phi-3
        "prompt": PROMPT_PHI3,
        "stop": ["<|end|>"]
    }
]

def get_ram_gb():
    return psutil.Process().memory_info().rss / (1024 ** 3)

print(f"{'Model':<22} | {'Threads':<8} | {'Speed (t/s)':<12} | {'RAM (GB)':<10}")
print("-" * 65)

for model_conf in MODELS:
    if not os.path.exists(model_conf["path"]):
        print(f"Skipping {model_conf['name']} (File not found)")
        continue

    for n_threads in model_conf["threads"]:
        # CRITICAL: Force memory cleanup before loading next model
        gc.collect()
        
        try:
            llm = Llama(
                model_path=model_conf["path"],
                n_threads=n_threads,
                n_ctx=model_conf["n_ctx"],
                verbose=False
            )
            
            # Warmup
            llm("Test", max_tokens=1)
            
            # Benchmark
            start = time.time()
            output = llm(
                model_conf["prompt"], 
                max_tokens=100, 
                stop=model_conf["stop"]
            )
            duration = time.time() - start
            
            # Metrics
            tokens = output['usage']['completion_tokens']
            speed = tokens / duration
            ram = get_ram_gb()
            
            print(f"{model_conf['name']:<22} | {n_threads:<8} | {speed:<12.2f} | {ram:<10.2f}")
            
            # CRITICAL: Explicitly destroy the object to free RAM
            del llm
            
        except Exception as e:
            print(f"Error running {model_conf['name']}: {e}")

print("-" * 65)
