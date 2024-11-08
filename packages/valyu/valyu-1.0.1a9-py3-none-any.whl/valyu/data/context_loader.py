import json
import requests
from pydantic import BaseModel
from typing import List
from valyu.models.models import get_api_key

class ContextMatch(BaseModel):
    id: str
    index: str
    score: float
    text: str
    url: str

class ContextResponse(BaseModel):
    top_k_matches: List[ContextMatch]

class Context:
    BASE_API_URL = "https://api.valyu.network"

    def __init__(self, data_sources, credit_budget, api_key=None):
        self.data_sources = data_sources
        self.credit_budget = credit_budget
        self.api_endpoint = f"{self.BASE_API_URL}/v1/context"
        self.api_key = api_key or get_api_key()

    def fetch_context(self, query: str) -> ContextResponse:
        try:
            payload = {
                "query": query
            }
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
            response = requests.post(
                self.api_endpoint, 
                json=payload,
                headers=headers,
                verify=False 
            )
            response.raise_for_status()
            data = response.json()
            if "results" in data:
                matches = [ContextMatch(
                    id=match['_id'],
                    index=match['_index'],
                    score=match['_score'],
                    text=match['_source']['text'],
                    url=match['_source'].get('url', 'N/A')
                ) for match in data['results']]
                return ContextResponse(top_k_matches=matches)
            return None
        except Exception:
            return None
