from google import genai
import dotenv

dotenv.load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
api_key = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_gemini_response(prompt: str) -> str:
    stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    )

    full_response = ""
    for chunk in stream:
        if hasattr(chunk, 'text'):
            #print(chunk.text, end="", flush=True)  # Stream to console
            full_response += chunk.text
    #print()  # Newline after streaming
    return full_response

# For standalone testing
if __name__ == "__main__":
    print(get_gemini_response("Explain how AI works in a few words"))
