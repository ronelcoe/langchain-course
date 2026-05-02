from dotenv import load_dotenv
import os

def main():
    # Load variables from .env into the process environment.
    load_dotenv()
    print("Hello from langchain-course!")
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPEN_API_KEY")
    print("API key loaded:", bool(api_key))


if __name__ == "__main__":
    main()
