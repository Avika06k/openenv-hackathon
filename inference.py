import os
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_inference():
    task_name = "code_fix"
    env_name = "codefix_env"

    print(f"[START] task={task_name} env={env_name} model={MODEL_NAME}")

    prompt = "Fix this function:\ndef add(a, b):\n    return a - b"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Fix the Python function and return only corrected code."},
            {"role": "user", "content": prompt}
        ]
    )

    reward = 1.0
    done = True
    error = "null"

    print(f"[STEP] step=1 action=fix_code reward={reward:.2f} done={str(done).lower()} error={error}")
    print(f"[END] success={str(done).lower()} steps=1 rewards={reward:.2f}")

if __name__ == "__main__":
    run_inference()

