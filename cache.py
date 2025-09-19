import os
import json
import time
import requests
from config import HF_TOKEN, CACHE_FILE, CACHE_TTL

# internal cache memory
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        _model_cache = json.load(f)
else:
    _model_cache = {}


def save_cache():
    """Save cache on drive."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_model_cache, f, indent=2, ensure_ascii=False)


def clear_cache(model: str = None):
    """Delete cache (all of it or specific models)."""
    global _model_cache
    if model:
        if model in _model_cache:
            del _model_cache[model]
            print(f"Cache for model '{model}' deleted.")
        else:
            print(f"Model '{model}' not in cache.")
    else:
        _model_cache.clear()
        print("Cache cleared.")
    save_cache()


def get_model_type(model: str) -> str:
    """Identify model type (chat vs. text-generation) with caching."""
    now = time.time()
    if model in _model_cache:
        entry = _model_cache[model]
        if now - entry["timestamp"] < CACHE_TTL:
            return entry["type"]

    url = f"https://huggingface.co/api/models/{model}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {HF_TOKEN}"})

    if resp.status_code == 404:
        clear_cache(model)
        raise Exception(f"Model '{model}' does not exist (404). Cache cleared.")
    if resp.status_code != 200:
        raise Exception(f"Error loading model info ({resp.status_code}): {resp.text}")

    data = resp.json()
    model_type = data.get("pipeline_tag", "text-generation")

    # Heuristics: some models may use chat-API
    router_models = ["mistral", "mistralai", "mixtral", "llama", "gemma", "command-r"]
    if any(key in model.lower() for key in router_models):
        model_type = "chat"

    _model_cache[model] = {"type": model_type, "timestamp": now}
    save_cache()
    
    return model_type
