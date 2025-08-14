import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')

# Dataset Configuration
DEFAULT_DATASET_PATH = os.getenv('DEFAULT_DATASET_PATH', r"C:\dataset.csv")

# Database Configuration
DB_NAME = os.getenv('DB_NAME', 'prompt_feedback.db')

# Other Configuration Settings
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 800))
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.2')) 