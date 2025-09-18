from llm1.llm1_bot import get_gemini_response
from llm2.llm2_bot import get_ollama_response
import sys
import io

# Ensure UTF-8 output on Windows consoles that default to cp1252
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except Exception:
        pass

def _choose_model_and_strip_command(text: str, last_model: str) -> (str, str):
    if not isinstance(text, str):
        return ("gemini", "")
    lowered = text.lstrip()
    if lowered.startswith("/gemini"):
        return ("gemini", lowered.split(" ", 1)[1] if " " in lowered else "")
    if lowered.startswith("/ollama") or lowered.startswith("/llama"):
        return ("ollama", lowered.split(" ", 1)[1] if " " in lowered else "")
    # Round-robin default when no explicit command
    next_model = "ollama" if last_model == "gemini" else "gemini"
    return (next_model, text)

def start_conversation(initial_prompt="Hello!"):
    turn = 0
    message = initial_prompt
    last_model = "ollama"  # so first implicit turn goes to gemini

    while True:
        model, user_text = _choose_model_and_strip_command(message, last_model)
        if model == "gemini":
            print("\n🧠 Gemini says:")
            message = get_gemini_response(user_text)
        else:
            print("\n🦙 Ollama says:")
            message = get_ollama_response(user_text)
        last_model = model

        print(message)
        turn += 1

        if turn > 3 or (isinstance(message, str) and "stop" in message.lower()):
            break
