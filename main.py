from llm import llm
from logger import reset_conversation
from config import PRESET_PARAMS, LOG_DIR

def main():
    print("Bibliotheks-Chat gestartet! (Tippe 'reset' für neue Unterhaltung, 'exit' zum Beenden)\n")
   
    # Choose preset
    print("Verfügbare Presets:", ", ".join(PRESET_PARAMS.keys()))
    preset = input("Wähle ein Preset (oder leer für Standard): ").strip()
    if preset not in PRESET_PARAMS:
        preset = None
        preset_label = "standard"
        print("→ Standardparameter werden verwendet.\n")
    else:
        preset_label = preset
        print(f"→ Preset '{preset}' wird verwendet.\n")
        
    # Reset conversation and start log file
    reset_conversation(preset_label)

    # Chat loop
    while True:
        user_input = input("Du: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Beende den Chat. Auf Wiedersehen!")
            break
        elif user_input.lower() in ["reset", "neustart", "neu"]:
            reset_conversation(preset_label)
            continue

        try:
            answer = llm(user_input, preset=preset)
            print(f"Assistent: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
