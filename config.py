import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please create a .env file with your OpenAI API key. "
        "See env_template.txt for the required format."
    )
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')

# Dataset Configuration
DEFAULT_DATASET_PATH = os.getenv('DEFAULT_DATASET_PATH', "cleaned_file.csv")

# Database Configuration
DB_NAME = os.getenv('DB_NAME', 'prompt_feedback.db')

# Other Configuration Settings
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 800))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.2)) 