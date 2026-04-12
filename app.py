from fastapi import FastAPI
from inference import reset_env, step_env

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/reset")
def reset():
    return reset_env()

@app.post("/step")
def step():
    return step_env()
