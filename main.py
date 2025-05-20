from fastapi import FastAPI, Depends, HTTPException
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

ollamaServer = os.getenv("OLLAMA_SERVER_URL") or ""
model = os.getenv("OLLAMA_MODEL_ID") or ""

app = FastAPI()
client = ollama.Client(ollamaServer)

@app.post("/generate")
def generate(prompt: str):
    response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}