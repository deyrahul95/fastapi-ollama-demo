from fastapi import FastAPI, Depends, HTTPException, Header, Request
from datetime import datetime, timedelta
import ollama
import os
from dotenv import load_dotenv
from http import HTTPStatus
from typing import Dict
import pytz
import re

load_dotenv()

ollamaServer = os.getenv("OLLAMA_SERVER_URL") or ""
model = os.getenv("OLLAMA_MODEL_ID") or ""

CREDITS : Dict[str, Dict] = {}
MAX_CREDITS = 3
TIMEZONE = pytz.timezone("UTC")

app = FastAPI()
client = ollama.Client(ollamaServer)

def get_today_key() -> str:
    today = datetime.now(TIMEZONE).date()
    return str(today)

def get_client_ip(request: Request) -> str:
    ip = request.client.host if request.client else "unknown_ip"
    return str(ip)

def reset_credits(ip: str):
    today_key = get_today_key()
    if ip not in CREDITS:
        CREDITS[ip] = {"credits": MAX_CREDITS, "last_reset": today_key}
    elif CREDITS[ip]["last_reset"] != today_key:
        CREDITS[ip] = {"credits": MAX_CREDITS, "last_reset": today_key}

def verify_Api_key(request: Request, x_api_key: str = Header(None)) -> str:
    ip = get_client_ip(request=request)

    if x_api_key is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Please provide api key")
    
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid api key")
    
    credit_info = CREDITS.get(ip, None)
    print(credit_info)

    if credit_info is None or credit_info["credits"] <= 0:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="No credits left! Please add credits before query.")
    
    return ip

@app.post("/generate")
def generate(prompt: str, ip: str = Depends(verify_Api_key)):
    CREDITS[ip]["credits"] -= 1
    
    response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]

    formattedContent = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    return {"response": formattedContent.strip()}

@app.get("/credits")
async def get_credits(request: Request, x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Please provide api key")
    
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid api key")
    
    ip = get_client_ip(request=request)

    reset_credits(ip=ip)
    
    return {"remaining_credits": CREDITS[ip]["credits"]}