from fastapi import APIRouter, Depends
from http import HTTPStatus

from src.constants.secrets import MODEL_ID, OLLAMA_SERVER_URL
from src.middlewares.auth import get_client_ip, verify_Api_key
from src.services.credit_service import CreditService
from src.services.ollama_service import OllamaService


router = APIRouter(prefix="/ollama", tags=["Ollama"])

ollama_service = OllamaService(model_url=OLLAMA_SERVER_URL, model_id=MODEL_ID)

@router.post("/generate", status_code=HTTPStatus.OK)
def generate(prompt: str, _ = Depends(verify_Api_key), 
            ip: str = Depends(get_client_ip), 
            creditService: CreditService = Depends(CreditService)):
    creditService.verify_credits(ip=ip)
    
    response = ollama_service.chat(query=prompt)
    tokens = len(response.split(" "))
    creditService.credit_used(ip=ip,tokens=tokens)

    return {"response": response}

@router.get("/credits", status_code=HTTPStatus.OK)
async def get_credits(_ = Depends(verify_Api_key), ip: str = Depends(get_client_ip), authService: CreditService = Depends(CreditService)):
    authService.reset_credits(ip=ip)
    
    return {"remaining_credits": round(authService.get_remaining_credits(ip=ip), 2)}

