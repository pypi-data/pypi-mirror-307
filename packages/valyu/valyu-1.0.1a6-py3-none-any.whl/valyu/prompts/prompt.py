from typing import Any, Dict
from valyu.data.context_loader import Context
from pydantic import BaseModel

class LLMResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] | None = None

class PromptTemplate:
    def __init__(self, template):
        self.template = template

    def enrich_and_invoke(self, context: Context, prompt: str, llm) -> LLMResponse:
        enriched_context = context.fetch_context(prompt)
        
        if enriched_context:
            context_str = "\n".join([f"{match.text}" for match in enriched_context.top_k_matches])
            filled_prompt = self.template.format(context=context_str, prompt=prompt)
            documents = [{"id": match.id, "text": match.text} for match in enriched_context.top_k_matches]
            
            print("\nGenerating response...")
            llm_response = llm.generate(filled_prompt, documents)
            
            self.display_response_with_citations(llm_response, enriched_context.top_k_matches)
            return self.format_response_with_citations(llm_response, enriched_context.top_k_matches)
        else:
            print("\nFailed to fetch context. Generating response without context.")
            llm_response = llm.generate(prompt, [])
            return LLMResponse(response=llm_response.get("text", ""), metadata=None)

    def display_response_with_citations(self, response_data, matches):
        response_text = response_data.get("text", "")
        citations = response_data.get("citations", [])
        
        print("\n" + "="*50)
        print("Response:")
        print("="*50)
        print(response_text)
        print("\n" + "="*50)
        
        # Only show cited documents
        cited_doc_ids = set()
        for citation in citations:
            cited_doc_ids.update(citation['document_ids'])
        
        cited_matches = [match for match in matches if match.id in cited_doc_ids]
        
        if cited_matches:
            print("\nSources:")
            print("-"*50)
            for idx, match in enumerate(cited_matches, 1):
                print(f"[{idx}] {match.url}")
            print("-"*50)

    def format_response_with_citations(self, response_data, matches):
        return LLMResponse(response=response_data.get("text", ""), metadata=response_data)
