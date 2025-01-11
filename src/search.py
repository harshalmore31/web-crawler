import asyncio
import aiohttp
import json
import time
from typing import List, Dict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
import os
from .config import config
from .process import url_processor
from .summarize import summarizer

console = Console()

class SearchEngine:
    def __init__(self):
        self.outputs_dir = config.outputs_dir
    
    async def fetch_search_results(self, query: str, progress: Progress) -> List[Dict]:
        """Fetch top search results using Google Custom Search API"""
        task_id = progress.add_task("[cyan]Fetching search results...", total=None)
        
        async with aiohttp.ClientSession() as session:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": config.google_api_key,
                "cx": config.google_cx,
                "q": query,
                "num": config.max_results
            }
            
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        for item in data.get("items", []):
                            if "link" in item and not any(x in item["link"].lower() for x in [".pdf", ".doc", ".docx"]):
                                results.append({
                                    "title": item.get("title", ""),
                                    "link": item["link"],
                                    "snippet": item.get("snippet", "")
                                })
                        progress.update(task_id, completed=True)
                        return results[:config.max_results]
                    else:
                        progress.update(task_id, completed=True, description="[red]Error in search")
                        console.print(f"[red]Error: {response.status} - {await response.text()}[/red]")
                        return []
            except Exception as e:
                progress.update(task_id, completed=True, description="[red]Error in search")
                console.print(f"[red]Error fetching search results: {str(e)}[/red]")
                return []
    
    async def search(self, query: str) -> str:
        """Main search function with timing"""
        start_time = time.time()
        
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=True
        )
        
        with progress:
            # Fetch search results
            search_results = await self.fetch_search_results(query, progress)
            if not search_results:
                return "No search results found."
            
            # Extract URLs
            urls = [result["link"] for result in search_results]
            
            # Process URLs concurrently
            extract_task = progress.add_task("[cyan]Extracting content...", total=None)
            extracted_data = await url_processor.process_urls_concurrent(urls, progress)
            progress.update(extract_task, completed=True)
            
            # Generate summary
            summary_task = progress.add_task("[cyan]Generating summary...", total=None)
            summary = await summarizer.summarize(extracted_data, query)
            progress.update(summary_task, completed=True)
            
            # Save results
            save_task = progress.add_task("[cyan]Saving results...", total=None)
            results = {
                "query": query,
                "search_results": search_results,
                "extracted_data": extracted_data,
                "summary": summary,
                "execution_time": time.time() - start_time
            }
            
            os.makedirs(self.outputs_dir, exist_ok=True)
            with open(os.path.join(self.outputs_dir, "search_results.json"), "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            progress.update(save_task, completed=True)
        
        return summary