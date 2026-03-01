from openai import OpenAI
from functools import lru_cache
from typing import List


class EmbeddingService:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    @lru_cache(maxsize=1000)
    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding
