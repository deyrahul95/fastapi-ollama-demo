import os
from dotenv import load_dotenv

load_dotenv()


OLLAMA_SERVER_URL: str = os.getenv("OLLAMA_SERVER_URL") or ""
MODEL_ID: str = os.getenv("OLLAMA_MODEL_ID") or ""
API_KEY: str = os.getenv("API_KEY") or ""
