import os
from datetime import datetime
from config import LOG_DIR, SYSTEM_PROMPT

# global state
conversation = [{"role": "system", 
                 "content": SYSTEM_PROMPT}]

current_log_file = None


def log_message(role: str, content: str):
    """Writes new message in current log file."""
    global current_log_file
    
    if not current_log_file:
        return

    with open(current_log_file, "a", encoding="utf-8") as f:
        f.write(f"{role.capitalize()}: {content}\n")


def reset_conversation(preset: str = "standard"):
    """Starts new conversation and creates new log file."""
    global conversation, current_log_file
   
    conversation = [{"role": "system", 
                     "content": SYSTEM_PROMPT}]
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_log_file = os.path.join(LOG_DIR, f"conversation_{timestamp}.log")
    
    with open(current_log_file, "w", encoding="utf-8") as f:
        f.write(f"New conversation has started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")        
        f.write(f"Preset: {preset}\n")
        f.write("=" * 60 + "\n")
    
    print(f"New conversation has started. Log file: {current_log_file} (Preset: {preset})")
