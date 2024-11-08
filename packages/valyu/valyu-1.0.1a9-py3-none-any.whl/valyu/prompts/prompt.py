from typing import Any, Dict
import sys
import time
from valyu.data.context_loader import Context
from pydantic import BaseModel
from rich.console import Console

console = Console()

class LLMResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] | None = None

class PromptTemplate:
    def __init__(self, template):
        self.template = template

    def enrich_and_invoke(self, context: Context, prompt: str, llm) -> LLMResponse:
        if context.data_sources != ["valyu/arxiv-papers"]:
            print("Error: No context available for this data source.")
            return LLMResponse(response="Error: No context available for this data source.", metadata=None)
        if context.credit_budget <= 100:
            print("Error: Not enough credits to fetch context.")
            return LLMResponse(response="Error: Not enough credits to fetch context.", metadata=None)
        
        if llm.model != "claude-3-sonnet":
            print("Error: Unsupported model. Currently only claude-3-sonnet is supported.")
            return LLMResponse(response="Error: Unsupported model.", metadata=None)
        
        enriched_context = context.fetch_context(prompt)
        
        if enriched_context:
            context_str = "\n".join([f"{match.text}" for match in enriched_context.top_k_matches])
            filled_prompt = self.template.format(context=context_str, prompt=prompt)
            documents = [{"id": match.id, "text": match.text} for match in enriched_context.top_k_matches]
            
            with console.status("[bold white]Thinking...[/bold white]"):
                llm_response = llm.generate(filled_prompt, documents)
            self._stream_response(llm_response, enriched_context.top_k_matches)
            return self.format_response_with_citations(llm_response, enriched_context.top_k_matches)
        else:
            with console.status("[bold white]Thinking...[/bold white]"):
                llm_response = llm.generate(prompt, [])
            self._stream_response(llm_response, [])
            return LLMResponse(response=llm_response.get("text", ""), metadata=None)

    def _stream_response(self, response_data, matches):
        response_text = response_data.get("text", "")
        citations = response_data.get("citations", [])
        
        # Stream the response
        print()
        for char in response_text:
            print(char, end='', flush=True)
            time.sleep(0.005) 
        print("\n")
        
        # Show unique sources if available
        cited_doc_ids = set()
        for citation in citations:
            cited_doc_ids.update(citation['document_ids'])
        
        # Deduplicate matches by URL while preserving order
        seen_urls = set()
        unique_matches = []
        for match in matches:
            if match.id in cited_doc_ids and match.url not in seen_urls:
                unique_matches.append(match)
                seen_urls.add(match.url)
        
        if unique_matches:
            print("\nSources:")
            print("-"*50)
            for idx, match in enumerate(unique_matches, 1):
                print(f"[{idx}] {match.url}")
            print("-"*50)

    def format_response_with_citations(self, response_data, matches):
        return LLMResponse(response=response_data.get("text", ""), metadata=response_data)
