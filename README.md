English version soon
# Chatbot für Bibliotheken
Kleiner Prototyp eines Assistenten für Bibliotheken auf Basis der Großen Sprachmodelle von [huggingface.co](huggingface.co). Standardmäßig wird das Modell `Mistral-Small-24B-Instruct-2501` genutzt. Der Bot antwortet auf Deutsch, Gespräche werden im Ordner `logs/` gespeichert.
## Installation
### Abhängigkeiten installieren
Benötigt werden `requests` und `dotenv`. Zum installieren: `pip install -r requirements.txt`
### Token festlegen
Damit die API von Huggingface angesprochen werden kann, wird ein Token benötigt, der in der Datei `.env` als `HF_TOKEN=hf_xxxxxxxxx` im Ordner des Skripts abgelegt werden muss.
## Konfiguration (optional)
Über `config.py` veränderbar:  
- `HF_TOKEN`: Wird aus `.env` geladen
- `MODEL`: Genutztes Sprachmodell. Ob die Chat-API oder die Inference-API von Huggingface benutzt werden sollen, sollte automatisch ermittelt werden (Standard: `mistralai/Mistral-Small-24B-Instruct-2501`).
- `GENERATION_PARAMS`: Einstellungen für Textgenerierung:
  + `max_tokens`: Höchstzahl der maximal ausgegebenen Tokens (Standard: 500).
  + `temperature`: Legt den Grad an Kreativität zwischen 1 (kreativ) und 0 (konservativ) fest (Standard: 0.5).
  + `top_p`: Wahrscheinlichkeitswert, der von allen Token addiert zwischen 1 (kreativ) und 0 (konservativ) erreicht werden muss (Standard: 0.95).
  + `top_k`: Anzahl k der wahrscheinlichsten Token, die im Generierungsschritt genutzt werden (Standard: 50).

## Ausführen
Zum Ausführen müssen alle Dateien im selben Ordner liegen. `main.py` ausführen, um den Chatbot zu starten.
