from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

ollamaServer = os.getenv("OLLAMA_SERVER_URL") or ""
model = os.getenv("OLLAMA_MODEL_ID") or ""

API_KEY_CREDITS = {os.getenv("API_KEY"): 3}

app = FastAPI()
client = ollama.Client(ollamaServer)


def verify_Api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)

    if credits <= 0:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="No credits left for this api key. Please add credits before query.")
    
    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_Api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}