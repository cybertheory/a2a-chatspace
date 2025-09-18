import sys
import os
import subprocess

def _ensure_dependencies() -> None:
    try:
        from google import genai  # noqa: F401
    except Exception:
        subprocess.run([sys.executable, "-m", "pip", "install", "google-genai>=0.3.0"], check=False)
    try:
        import dotenv  # noqa: F401
    except Exception:
        subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv>=1.0.1"], check=False)

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    _ensure_dependencies()
    if os.getenv("RUN_BRIDGE", "0") == "1":
        # Lazy install mautrix when running bridge
        try:
            import mautrix  # noqa: F401
        except Exception:
            subprocess.run([sys.executable, "-m", "pip", "install", "mautrix"], check=False)
        from bridge_app import run_bridge_blocking
        run_bridge_blocking()
    else:
        from router.message_router import start_conversation
        start_conversation("Hi there!")
