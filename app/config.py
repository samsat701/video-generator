import os
from google.generativeai import configure
from dotenv import load_dotenv

# Load environment variables from .env file, if it exists
load_dotenv()

# Set up your API key for Gemini
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("No API key found. Please set the API_KEY environment variable.")
configure(api_key=GOOGLE_API_KEY)
