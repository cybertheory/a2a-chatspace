from llm1_bot import get_gemini_response
from llm2_bot import get_ollama_response

def start_conversation(initial_prompt="Hello!"):
    turn = 0
    message = initial_prompt

    while True:
        if turn % 2 == 0:
            print("\n🧠 Gemini says:")
            message = get_gemini_response(message)
        else:
            print("\n🦙 Ollama says:")
            message = get_ollama_response(message)

        print(message)
        turn += 1

        if turn > 10 or "stop" in message.lower():
            break
