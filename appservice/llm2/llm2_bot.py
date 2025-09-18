import subprocess
import sys
try:
    import ollama
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "ollama"], check=False)
_OLLAMA_AVAILABLE = True

model_name = 'llama2'

class _DummyMessage:
    def __init__(self, content):
        self.content = content

class _DummyResponse:
    def __init__(self, text):
        self.message = _DummyMessage(text)

def chat(model, messages):
    if _OLLAMA_AVAILABLE and hasattr(ollama, 'chat'):
        return ollama.chat(model=model, messages=messages, stream=True)
    install_msg = (
        "ollama is not available.\n"
        "Install the Ollama runtime and Python client, then ensure the 'ollama' CLI is on your PATH.\n"
        "Quick steps:\n"
        " 1) Install the Ollama app / runtime: https://ollama.ai\n"
        " 2) Install the Python client: python -m pip install ollama\n"
        " 3) Verify you can run 'ollama' from your shell and import ollama in Python.\n"
    )
    return _DummyResponse(install_msg)

def get_ollama_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    stream = ollama.chat(model=model_name, messages=messages, stream=True)

    full_response = ""
    for chunk in stream:
        content = chunk.get("message", {}).get("content", "")
        #print(content, end="", flush=True)  # Stream to console
        full_response += content
    #print()  # Newline after streaming

    return full_response


# For standalone testing
if __name__ == "__main__":
    print(get_ollama_response("Hello!"))
