from logger import reset_conversation
from llm import llm

if __name__ == "__main__":
    print("Bibliotheks-Chat gestartet! (Tippe 'reset' für neue Unterhaltung, 'exit' zum Beenden)\n")
    reset_conversation()

    while True:
        user_input = input("Du: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Auf Wiedersehen!")
            break

        if user_input.lower() in ["reset", "neustart", "neu"]:
            reset_conversation()
            continue

        try:
            answer = llm(user_input)
            print(f"Assistent: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")
