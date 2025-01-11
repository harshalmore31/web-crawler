import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # API Keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Directory configuration
        self.outputs_dir = "outputs"
        os.makedirs(self.outputs_dir, exist_ok=True)
        
        # Search configuration
        self.max_results = 10
        
        # Processing configuration
        self.max_retries = 3
        self.max_threads = 10
        self.timeout = 15
        
        # Browser configuration
        self.viewport = {'width': 1920, 'height': 1080}
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration values"""
        required_env_vars = {
            "GOOGLE_API_KEY": self.google_api_key,
            "GOOGLE_CX": self.google_cx,
            "GEMINI_API_KEY": self.gemini_api_key
        }
        
        missing_vars = [var for var, value in required_env_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

config = Config()