
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/log")
def get_logs():
    with open("data/log.jsonl") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]
