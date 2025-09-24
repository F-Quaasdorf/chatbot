import requests
from config import HF_TOKEN, MODEL, GENERATION_PARAMS
from cache import get_model_type, clear_cache
from logger import conversation, log_message
from config import HF_TOKEN, MODEL, GENERATION_PARAMS, PRESET_PARAMS

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}",
           "Content-Type": "application/json"}


def llm(query: str, model: str = MODEL, preset: str = None) -> str:
    global conversation
    conversation.append({"role": "user", "content": query})
    log_message("User", query)

    # Parameter auswählen
    params = GENERATION_PARAMS.copy()
    if preset and preset in PRESET_PARAMS:
        params = PRESET_PARAMS[preset].copy()

    model_type = get_model_type(model)

    try:
        if model_type in ["chat", "conversational", "text2text-generation"]:
            # Chat-API
            url = "https://router.huggingface.co/together/v1/chat/completions"
            payload = {"model": model,
                       "messages": conversation,
                       **params}

            resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)

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
                                      **params}}

            resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)

    except requests.exceptions.Timeout:
        error_msg = "Error: Response from Hugging Face took too long (Timeout)."
        log_message("System", error_msg)
        return error_msg
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error: {e}"
        log_message("System", error_msg)
        return error_msg

    # HTTP-Status prüfen
    if resp.status_code == 404:
        clear_cache(model)
        error_msg = f"Error: Model '{model}' not found (404). Cache cleared."
        log_message("System", error_msg)
        return error_msg
    
    if resp.status_code != 200:
        error_msg = f"Error {resp.status_code}: {resp.text}"
        log_message("System", error_msg)
        return error_msg

    # JSON-Parsing prüfen
    try:
        data = resp.json()
    except ValueError:
        error_msg = "Error: Response could not be read as JSON."
        log_message("System", error_msg)
        return error_msg

    # Antwort extrahieren
    try:
        if model_type in ["chat", "conversational", "text2text-generation"]:
            answer = data["choices"][0]["message"]["content"].strip()
        else:
            answer = data[0]["generated_text"].strip()
    except (KeyError, IndexError, TypeError) as e:
        error_msg = f"Fehler beim Verarbeiten der Antwort: {e}"
        log_message("System", error_msg)
        return error_msg

    conversation.append({"role": "assistant", "content": answer})
    log_message("Assistant", answer)
    
    return answer
