import time
from llama_cpp import Llama

# 1. Initialize the Model
# n_ctx=2048:  The "memory" of the conversation (context window).
# n_threads=4: We are using all 4 vCPUs of your D4s_v3.
print("Loading model...")
start_load = time.time()
llm = Llama(
    model_path="./mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4, 
    verbose=False
)
print(f"Model loaded in {time.time() - start_load:.2f} seconds.")

# 2. Define the Prompt
prompt = "Q: Explain the concept of 'Recursion' in programming to a high school student. A: "

# 3. Run Inference
print("Generating response...")
start_gen = time.time()
output = llm(
    prompt, 
    max_tokens=200, # Limit response length
    stop=["Q:", "\n"], # Stop if it tries to ask a new question
    echo=True 
)
end_gen = time.time()

# 4. Print Result & Stats
print("\n" + "="*50)
print(output['choices'][0]['text'])
print("="*50 + "\n")

# Calculate Speed
tokens = output['usage']['completion_tokens']
duration = end_gen - start_gen
print(f"Generated {tokens} tokens in {duration:.2f} seconds.")
print(f"Speed: {tokens / duration:.2f} tokens/second")
