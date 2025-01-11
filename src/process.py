from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from .config import config
from .extract_content import content_extractor

class URLProcessor:
    def __init__(self):
        self.max_threads = config.max_threads
    
    def process_url(self, url: str, progress: Progress, task_id: int) -> Optional[Dict]:
        """Process a single URL"""
        try:
            result = content_extractor.extract_content(url)
            if result:
                progress.update(task_id, advance=1)
            return result
        except Exception as e:
            print(f"Failed to process {url}: {str(e)}")
            progress.update(task_id, advance=1)
            return None
    
    async def process_urls_concurrent(self, urls: List[str], parent_progress: Progress = None) -> List[Dict]:
        """Process multiple URLs concurrently using ThreadPoolExecutor"""
        successful_results = []
        
        progress = parent_progress or Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
        )
        
        task_id = progress.add_task("[cyan]Processing websites...", total=len(urls))
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_url = {
                executor.submit(self.process_url, url, progress, task_id): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        successful_results.append(result)
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")
        
        progress.update(task_id, completed=True)
        return successful_results

url_processor = URLProcessor()