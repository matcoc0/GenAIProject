"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    {
        "model_name": "deepseek-r1:7b",
        "flask_url": os.getenv("DEEPSEEK_URL")
    },
    # {
    #     "model_name": "LLM2",
    #     "flask_url": os.getenv("LLM2_URL")
    # },
    # {
    #     "model_name": "LLM3",
    #     "flask_url": os.getenv("LLM3_URL")
    # },
    # {
    #     "model_name": "LLM4",
    #     "flask_url": os.getenv("LLM4_URL")
    # }
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = {
    "model_name": "llama3.2:1b",
    "flask_url": os.getenv("CHAIRMAN_URL")
}

# Data directory for conversation storage
DATA_DIR = "data/conversations"