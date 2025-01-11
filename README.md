# Web Content Analysis Tool

A powerful tool for searching, extracting, and analyzing web content using Google Search, Playwright, and Gemini AI.

## Features

- Google Custom Search integration for finding relevant web pages
- Concurrent web content extraction using Playwright
- Content cleaning and processing
- AI-powered summarization using Google's Gemini
- Progress tracking and error handling

## Setup

1. Install dependencies:
```bash
pip install aiohttp beautifulsoup4 python-dotenv google-generativeai rich html2text playwright tenacity
```

2. Configure environment variables:
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX=your_google_cx
GEMINI_API_KEY=your_gemini_api_key
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

```python
from src.search import search

# Run a search query
result = search("your search query here")
```

## Project Structure

```
├── README.md
├── LICENSE
└── src/
    ├── config.py          # Configuration and environment variables
    ├── extract_content.py # Web content extraction logic
    ├── process.py         # URL processing and concurrency handling
    ├── search.py         # Main search functionality
    └── summarize.py      # AI summarization using Gemini
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.