from datetime import datetime
from http import HTTPStatus
from fastapi import HTTPException
from typing import Dict, TypedDict

from src.constants.defaults import MAX_CREDITS, TIMEZONE


class CreditInfo(TypedDict):
    credits: int
    last_reset: str


class CreditService:
    """Service to manage per-IP usage credits with daily reset logic."""

    _credits: Dict[str, CreditInfo] = {}

    def verify_credits(self, ip: str) -> bool:
        """
        Verify if the given IP address has any remaining credits.

        Args:
            ip (str): The IP address of the requester.

        Raises:
            HTTPException: If the requester has no remaining credits.

        Returns:
            bool: True if credits are available.
        """
        credit_info = self._credits.get(ip)

        if credit_info is None or credit_info["credits"] <= 0:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="No credits left! Please add credits before query."
            )

        return True

    def credit_used(self, ip: str) -> None:
        """
        Decrease the credit count for a given IP.

        Args:
            ip (str): The IP address using a credit.
        """
        if ip in self._credits:
            self._credits[ip]["credits"] -= 1

    def get_remaining_credits(self, ip: str) -> int:
        """
        Get the number of remaining credits for a given IP.

        Args:
            ip (str): The IP address to query.

        Returns:
            int: The number of remaining credits.
        """
        return self._credits.get(ip, {}).get("credits", 0)

    def get_today_key(self) -> str:
        """
        Get a string key representing today's date.

        Returns:
            str: Today's date in ISO format (YYYY-MM-DD).
        """
        return datetime.now(TIMEZONE).date().isoformat()

    def reset_credits(self, ip: str) -> None:
        """
        Reset credits for the given IP if the last reset wasn't today.

        Args:
            ip (str): The IP address to reset.
        """
        today_key = self.get_today_key()
        current_data = self._credits.get(ip)

        if current_data is None or current_data["last_reset"] != today_key:
            self._credits[ip] = {"credits": MAX_CREDITS, "last_reset": today_key}
