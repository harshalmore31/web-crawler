from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import html2text
from typing import Optional, Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from .config import config

class ContentExtractor:
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = True
        self.html_converter.ignore_images = True
        self.html_converter.ignore_emphasis = True
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_content(self, url: str) -> Optional[Dict]:
        """Extract content from a URL with retry mechanism"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport=config.viewport,
                    user_agent=config.user_agent
                )
                
                page = context.new_page()
                page.set_default_timeout(25000)
                
                page.goto(url)
                page.wait_for_load_state('networkidle', timeout=20000)
                
                # Extract content
                content = page.content()
                soup = BeautifulSoup(content, 'lxml')
                
                # Clean up content
                for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                    element.decompose()
                
                # Get main content
                main_content = soup.find('main') or soup.find('article') or soup.find('div', {'class': ['content', 'main']})
                if not main_content:
                    main_content = soup.find('body')
                
                # Convert to markdown-like text
                clean_text = self.html_converter.handle(str(main_content))
                
                browser.close()
                
                return {
                    "url": url,
                    "title": soup.title.string if soup.title else "No title",
                    "content": clean_text.strip()
                }
                
        except Exception as e:
            print(f"Warning: Failed to extract from {url}: {str(e)}")
            return None

content_extractor = ContentExtractor()