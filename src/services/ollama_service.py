import ollama
import re

from src.services.cache_service import CacheService


class OllamaService:
    def __init__(self, model_url: str, model_id: str):
        """
        Initialize the Ollama service with the model URL.
        """
        self.model_url = model_url
        self.model_id = model_id
        self.client = ollama.Client(model_url)
        self.cache_service = CacheService()

    def chat(self, query: str) -> str:
        """
        Method to send a query to the Ollama model.
        """
        try:
            cached_response = self.cache_service.get_cached_response(query=query)
            if cached_response:
                return cached_response

            response = self.client.chat(
                model=self.model_id, messages=[{"role": "user", "content": query}]
            )
            content = response["message"]["content"]

            formattedContent = re.sub(
                r"<think>.*?</think>", "", content, flags=re.DOTALL
            ).strip()
            self.cache_service.set_cache(query=query, response=formattedContent)

            return formattedContent
        except Exception as e:
            print(f"Error while connecting to Ollama service: {e}")
            return "Failed to get response from Ollama service"
