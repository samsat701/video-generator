import os
from google.generativeai import configure

# Set up your API key for Gemini
API_KEY = os.getenv('API_KEY', 'your_default_api_key')
configure(api_key=API_KEY)
