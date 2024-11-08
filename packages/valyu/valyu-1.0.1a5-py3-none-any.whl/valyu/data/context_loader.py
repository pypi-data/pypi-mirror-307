import json
import requests
from pydantic import BaseModel
from typing import List
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

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

    def __init__(self, data_sources, credit_budget, api_key):
        self.data_sources = data_sources
        self.credit_budget = credit_budget
        self.api_endpoint = f"{self.BASE_API_URL}/v1/context"
        self.api_key = api_key

    def fetch_context(self, query: str) -> ContextResponse:
        console.print(Panel(f"🔍 Fetching context for query: [bold]{query}[/bold]", style="bold blue"))
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
                console.print(Panel(f"✅ Context fetched successfully. {len(matches)} documents retrieved.", style="bold green"))
                return ContextResponse(top_k_matches=matches)
            else:
                console.print("[bold red]Unexpected response format[/bold red]")
                return None
        except Exception as e:
            console.print(f"[bold red]Error fetching context: {e}[/bold red]")
            if hasattr(e, 'response') and e.response is not None:
                console.print(f"[bold red]Error response: {e.response.text}[/bold red]")
            return None
