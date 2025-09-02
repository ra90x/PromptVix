"""Configuration settings for PromptVix application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY environment variable is not set. "
        "Please create a .env file with your OpenRouter API key. "
        "See env_template.txt for the required format."
    )

# Available LLM Models
AVAILABLE_MODELS = {
    "DeepSeek v3.1": "deepseek/deepseek-chat-v3.1",
    "OpenAI GPT-4o": "openai/chatgpt-4o-latest",
    "Claude 3.7 Sonnet": "anthropic/claude-3.7-sonnet"
}

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Supabase Configuration
SUPABASE_URL = os.getenv(
    'SUPABASE_URL', 
    'https://nafxymsdbtdxkjknorvl.supabase.co'
)
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_ANON_KEY:
    raise ValueError(
        "SUPABASE_ANON_KEY environment variable is not set. "
        "Please create a .env file with your Supabase credentials. "
        "See env_template.txt for the required format."
    )

# Dataset Configuration
DEFAULT_DATASET_PATH = os.getenv(
    'DEFAULT_DATASET_PATH', 
    "Superstore_Dataset.csv"
)

# Other Configuration Settings
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 800))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.2)) 
