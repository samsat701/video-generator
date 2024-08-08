from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-1.5-flash')

def generate_script(prompt):
    response = model.generate_content(prompt)
    return response.text
