import json
from valyu.data.context_loader import Context
from pydantic import BaseModel
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from typing import Any, Dict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

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
            
            console.print("\n")
            
            with console.status("[bold green]Thinking...[/bold green]") as status:
                llm_response = llm.generate(filled_prompt, documents)
            
            self.display_response_with_citations(llm_response, enriched_context.top_k_matches)
            return self.format_response_with_citations(llm_response, enriched_context.top_k_matches)
        else:
            console.print("[bold red]Failed to fetch context. Generating response without context.[/bold red]")
            llm_response = llm.generate(prompt, [])
            return LLMResponse(response=llm_response.get("text", ""), metadata=None)

    def display_response_with_citations(self, response_data, matches):
        response_text = response_data.get("text", "")
        citations = response_data.get("citations", [])
        
        text = Text()
        panel = Panel(text, border_style="green", expand=True)
        
        console.print("\n[bold green]Response with Citations[/bold green]")
        
        # Create doc_map only for documents that are actually cited
        cited_doc_ids = set()
        for citation in citations:
            cited_doc_ids.update(citation['document_ids'])
        
        # Only map documents that are actually cited
        doc_map = {
            match.id: f"doc{index+1}" 
            for index, match in enumerate(matches) 
            if match.id in cited_doc_ids
        }
        
        with Live(panel, refresh_per_second=20, console=console) as live:
            last_end = 0
            current_text = ""
            
            for citation in sorted(citations, key=lambda x: x['start']):
                pre_citation = response_text[last_end:citation['start']]
                current_text += pre_citation
                text.plain = current_text
                live.update(panel)
                
                cited_text = response_text[citation['start']:citation['end']]
                current_text += cited_text
                text.plain = current_text
                text.stylize("bold yellow", len(current_text) - len(cited_text), len(current_text))
                live.update(panel)
                
                doc_refs = f"({','.join(doc_map[doc_id] for doc_id in citation['document_ids'])})"
                current_text += doc_refs
                text.plain = current_text
                text.stylize("bold blue", len(current_text) - len(doc_refs), len(current_text))
                live.update(panel)
                
                last_end = citation['end']
            
            remaining_text = response_text[last_end:]
            current_text += remaining_text
            text.plain = current_text
            live.update(panel)
        
        console.print("\n[dim]Citation Legend: [yellow]Highlighted text[/yellow] shows cited content, [blue](docX)[/blue] shows source document reference[/dim]\n")
        
        # Display only the cited documents in the key
        console.print("\n[bold]Document Key:[/bold]")
        cited_matches = [match for match in matches if match.id in cited_doc_ids]
        if cited_matches:
            console.print("\n[bold]📚 Sources:[/bold]")
            console.print("─" * 50)  # Add a separator line
            for match in cited_matches:
                doc_label = doc_map[match.id]
                console.print(f"[bold blue]{doc_label}[/bold blue] [white]•[/white] {match.url}")
            console.print("─" * 50)  # Add a separator line

    def format_response_with_citations(self, response_data, matches):
        response_text = response_data.get("text", "")
        citations = response_data.get("citations", [])
        formatted_response = response_text
        doc_map = {match.id: f"doc{index+1}" for index, match in enumerate(matches)}
        for citation in sorted(citations, key=lambda x: x['start'], reverse=True):
            doc_refs = f"({','.join(doc_map[doc_id] for doc_id in citation['document_ids'])})"
            formatted_response = (
                formatted_response[:citation['end']] + doc_refs + formatted_response[citation['end']:]
            )
        return LLMResponse(response=formatted_response, metadata=response_data)
