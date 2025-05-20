from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException

from src.constants.defaults import MAX_CREDITS, TIMEZONE

from typing import Dict


CREDITS : Dict[str, Dict] = {}


class CreditService:
    def verify_credits(self, ip: str) -> bool:
        credit_info = CREDITS.get(ip, None)

        if credit_info is None or credit_info["credits"] <= 0:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="No credits left! Please add credits before query.")
        
        return True
    
    def credit_used(self, ip: str):
        if ip in CREDITS:
            CREDITS[ip]["credits"] -= 1

    def get_remaining_credits(self, ip: str) -> int:
        if ip in CREDITS:
            return CREDITS[ip]["credits"]
        
        return 0

    def get_today_key(self) -> str:
        today = datetime.now(TIMEZONE).date()
        return str(today)

    def reset_credits(self, ip: str):
        today_key = self.get_today_key()
        if ip not in CREDITS:
            CREDITS[ip] = {"credits": MAX_CREDITS, "last_reset": today_key}
        elif CREDITS[ip]["last_reset"] != today_key:
            CREDITS[ip] = {"credits": MAX_CREDITS, "last_reset": today_key}
