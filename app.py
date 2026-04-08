from fastapi import FastAPI, HTTPException
from models import Action, Observation, State
from environment import CodeFixEnv
import os

app = FastAPI()

# Sample task
buggy_code = """
def add(a, b):
    return a - b
"""
test_cases = [
    "assert add(2, 3) == 5",
    "assert add(-1, 1) == 0"
]

env = CodeFixEnv("Add Function Fix", buggy_code, test_cases)

@app.post("/reset", response_model=Observation)
async def reset():
    return env.reset()

@app.post("/step", response_model=Observation)
async def step(action: Action):
    return env.step(action)

@app.get("/state", response_model=State)
async def get_state():
    return env.state

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "codefix-env"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
