import os
from dotenv import load_dotenv

# load .env (e.g. for HF_TOKEN)
load_dotenv()

# Hugging Face API-Token (from .env)
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set. Please set HF_TOKEN=YourTokenHere in .env")

# standard model: mistralai/Mistral-Small-24B-Instruct-2501
MODEL = "mistralai/Mistral-Small-24B-Instruct-2501"

# system prompt for Assistant
SYSTEM_PROMPT = "Du bist ein Bibliotheksassistent. Antworte immer auf Deutsch."

# Cache configuration
CACHE_FILE = "cache.json"
CACHE_TTL = 7 * 24 * 60 * 60  # 7 days

# Logging directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # makes sure that logs/ exists

# Standard parameters for text-generation
GENERATION_PARAMS = {"max_tokens": 500,
                     "temperature": 0.5,
                     "top_p": 0.95,
                     "top_k": 50}

# Alternative Presets
PRESET_PARAMS = {"creative": {"max_tokens": 800,
                              "temperature": 0.9,
                              "top_p": 0.95,
                              "top_k": 50},
                 
                 "precise": {"max_tokens": 400,
                             "temperature": 0.2,
                             "top_p": 0.9,
                             "top_k": 40},
                 
                 "long": {"max_tokens": 1500,
                          "temperature": 0.6,
                          "top_p": 0.95,
                          "top_k": 50}}
