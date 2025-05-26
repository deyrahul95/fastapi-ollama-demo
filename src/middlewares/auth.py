from http import HTTPStatus
from fastapi import HTTPException, Header, Request

from src.constants.secrets import API_KEY


def verify_Api_key(x_api_key: str = Header(None)) -> bool:
    if x_api_key is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Please provide api key"
        )

    if x_api_key != API_KEY:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid api key")

    return True


def get_client_ip(request: Request) -> str:
    ip = request.client.host if request.client else "unknown_ip"
    return str(ip)
