import asyncio
from typing import List, Dict
import google.generativeai as genai
from .config import config

class ContentSummarizer:
    def __init__(self):
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 4096,
            }
        )
    
    def _format_content(self, extracted_data: List[Dict], query: str) -> str:
        """Format content for summarization"""
        formatted_content = "# Source Materials:\n\n"
        for i, item in enumerate(extracted_data, 1):
            formatted_content += f"""
### Source {i}: {item['title']}
URL: {item['url']}

{item['content'][:2000]}  # Limit content length per source

---
"""
        return formatted_content
    
    def _create_prompt(self, formatted_content: str, query: str) -> str:
        """Create the summarization prompt"""
        return f"""
Analyze and summarize the following content about: "{query}"

Create a detailed summary with these sections:
1. Key Findings (2-3 paragraphs)
2. Important Details (bullet points)
3. Sources (numbered list)

Focus on accuracy, clarity, and completeness.
Present conflicting information if found.
Use proper markdown formatting.

Content to analyze:
{formatted_content}
"""
    
    async def summarize(self, extracted_data: List[Dict], query: str) -> str:
        """Generate summary using Gemini API"""
        formatted_content = self._format_content(extracted_data, query)
        prompt = self._create_prompt(formatted_content, query)
        
        response = await asyncio.to_thread(
            lambda: self.model.generate_content(prompt).text
        )
        
        return response

summarizer = ContentSummarizer()