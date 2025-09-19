import requests
from config import HF_TOKEN, MODEL, GENERATION_PARAMS
from cache import get_model_type, clear_cache
from logger import conversation, log_message

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}",
           "Content-Type": "application/json"}


def llm(query: str, model: str = MODEL) -> str:
    """Sends requests to LLM (Chat-API or Inference-API)."""
    global conversation
    conversation.append({"role": "user", "content": query})
    log_message("User", query)

    model_type = get_model_type(model)

    if model_type in ["chat", "conversational", "text2text-generation"]:
        # Chat-API
        url = "https://router.huggingface.co/together/v1/chat/completions"
        
        payload = {"model": model,
                   "messages": conversation,
                   **GENERATION_PARAMS}  # Variable from config.py
        
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        if resp.status_code == 404:
            clear_cache(model)
            raise Exception(f"Chat API 404: Model '{model}' does not exist. Cache cleared.")
        if resp.status_code != 200:
            raise Exception(f"Chat API error {resp.status_code}: {resp.text}")

        data = resp.json()
        answer = data["choices"][0]["message"]["content"].strip()

    else:
        # Inference-API
        history_text = ""
        
        for msg in conversation:
            if msg["role"] == "system":
                history_text += f"System: {msg['content']}\n"
            elif msg["role"] == "user":
                history_text += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                history_text += f"Assistant: {msg['content']}\n"
        
        history_text += "Assistant:"

        url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {"inputs": history_text,
                   "parameters": {"return_full_text": False,
                                  **GENERATION_PARAMS}} # Variable from config.py
        
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        if resp.status_code == 404:
            clear_cache(model)
            raise Exception(f"Inference API 404: Model '{model}' does not exist. Cache cleared.")
        if resp.status_code != 200:
            raise Exception(f"Inference API error {resp.status_code}: {resp.text}")

        data = resp.json()
        answer = data[0]["generated_text"].strip()

    conversation.append({"role": "assistant", "content": answer})
    log_message("Assistant", answer)
    
    return answer
