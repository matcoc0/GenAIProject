"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    {
        "model_name": "llama3.2:1b",
        "flask_url": os.getenv("CHAIRMAN_URL")
    },
    {
        "model_name": "gemma3:4b",
        "flask_url": os.getenv("GEMMA_URL")
    },
    {
        "model_name": "qwen2.5:1.5b",
        "flask_url": os.getenv("QWEN_URL")
    },
    {
        "model_name": "ministral-3:3b",
        "flask_url": os.getenv("MISTRAL_URL")
    }
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = {
    "model_name": "deepseek-r1:7b",
    "flask_url": os.getenv("DEEPSEEK_URL")
}

# Data directory for conversation storage
DATA_DIR = "data/conversations"