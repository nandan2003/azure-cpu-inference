import time
from llama_cpp import Llama

# Microsoft Phi-3 Mini (3.8B Parameters)
MODEL_PATH = "./Phi-3-mini-4k-instruct-q4.gguf"

print(f"--- LOADING PHI-3 MINI ---")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=3, # Use all 4 vCPUs
    verbose=False
)

# Phi-3 uses a specific prompt format
prompt = "<|user|>\nWrite a Python function to calculate the Fibonacci sequence.<|end|>\n<|assistant|>"

print("--- GENERATING ---")
start = time.time()
output = llm(prompt, max_tokens=200, stop=["<|end|>"])
end = time.time()

tokens = output['usage']['completion_tokens']
duration = end - start
speed = tokens / duration

print(f"\nModel: Phi-3 Mini (3.8B)")
print(f"Tokens Generated: {tokens}")
print(f"Time: {duration:.2f}s")
print(f"SPEED: {speed:.2f} tokens/sec")
print("-" * 30)
