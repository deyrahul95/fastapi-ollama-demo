from fastapi import APIRouter, Depends, Header, Request
from http import HTTPStatus

from src.constants.secrets import MODEL_ID, OLLAMA_SERVER_URL
from src.middlewares.auth import get_client_ip, verify_Api_key
from src.services.cache_service import CacheService
from src.services.credit_service import CreditService
from src.services.ollama_service import OllamaService


router = APIRouter(prefix="/ollama", tags=["Ollama"])

ollama_service = OllamaService(model_url=OLLAMA_SERVER_URL, model_id=MODEL_ID)

@router.post("/generate", status_code=HTTPStatus.OK)
def generate(prompt: str, _ = Depends(verify_Api_key), 
            ip: str = Depends(get_client_ip), 
            creditService: CreditService = Depends(CreditService), 
            cacheService: CacheService = Depends(CacheService)):
    creditService.verify_credits(ip=ip)

    creditService.credit_used(ip=ip)

    cached_response = cacheService.get_cached_response(query=prompt)
    if cached_response:
        return { "response": cached_response }
    
    response = ollama_service.chat(query=prompt)
    cacheService.set_cache(query=prompt, response=response)
    
    return {"response": response}

@router.get("/credits", status_code=HTTPStatus.OK)
async def get_credits(_ = Depends(verify_Api_key), ip: str = Depends(get_client_ip), authService: CreditService = Depends(CreditService)):
    authService.reset_credits(ip=ip)
    
    return {"remaining_credits": authService.get_remaining_credits(ip=ip)}

