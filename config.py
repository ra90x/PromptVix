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
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-v3.1-base')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Dataset Configuration
DEFAULT_DATASET_PATH = os.getenv('DEFAULT_DATASET_PATH', "cleaned_file.csv")

# Database Configuration
DB_NAME = os.getenv('DB_NAME', 'prompt_feedback.db')

# Other Configuration Settings
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 800))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.2)) 
