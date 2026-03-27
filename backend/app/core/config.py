import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Default model - you can change this later
MODEL_NAME = "llama-3.1-8b-instant"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env file")