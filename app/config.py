import os
from google.generativeai import configure

# Set up your API key for Gemini
API_KEY = os.getenv('API_KEY', 'AIzaSyA859D0AGFPZPVd5ysBL5KTHLIVsy5rCVg')
configure(api_key=API_KEY)