# Chatbot für Bibliotheken
Kleiner Prototyp eines Assistenten für Bibliotheken auf Basis der Großen Sprachmodelle von [huggingface.co](https://huggingface.co). Standardmäßig wird das Modell `Mistral-Small-24B-Instruct-2501` genutzt. Der Bot antwortet auf Deutsch, Gespräche werden im Ordner `logs/` gespeichert.
## Installation
### Abhängigkeiten installieren
Benötigt werden `requests` und `dotenv`. Installation via: 
```bash
pip install -r requirements.txt
```
### Token festlegen
Damit die API von Hugging Face angesprochen werden kann, wird ein Token benötigt. Der Token muss in der Datei `.env` im selben Ordner abgelegt werden:
```env
HF_TOKEN=hf_xxxxxxxxx
```
## Konfiguration
Die Konfiguration befindet sich in `config.py`.  
- `HF_TOKEN`: Wird aus `.env` geladen
- `MODEL`: Genutztes Sprachmodell. Standardmäßig wird die Chat-API verwendet. Der Aufruf der Inference-API ist möglich. Standard: `mistralai/Mistral-Small-24B-Instruct-2501`.
- `SYSTEM_PROMPT`: Vorgaben für das Sprachmodell. Standard: "Du bist ein Bibliotheksassistent. Antworte immer auf Deutsch."
- `GENERATION_PARAMS`: Einstellungen für Textgenerierung:
  + `max_tokens`: Maximallänge der Ausgabe (Standard: 500).
  + `temperature`: Kreativität (zwischen 0 = konservativ, 1 = sehr kreativ, Standard: 0.5).
  + `top_p`: Sampling nach Wahrscheinlichkeiten (zwischen 0 = deterministisch und 1 = kreativ, Standard: 0.95).
  + `top_k`: Anzahl der bei jedem Schritt berücksichtigten Token (Standard: 50).

Die folgenden Presets können ausgewählt werden, um die Standardeinstellungen für die Textgenerierung zu überschreiben:
- `creative`: Längere und kreativere Ausgaben.
- `precise`: Kürzere und präzisere Ausgaben.
- `long`: Lange Antworten.
## Ausführen
Zum Ausführen: 
```bash
python main.py
```
Danach kann ein Preset gewählt werden (ohne Auswahl werden die Standardeinstellungen verwendet). Konversationen und das verwendete Preset werden im Ordner `logs/` protokolliert.
