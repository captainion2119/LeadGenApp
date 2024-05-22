import google.generativeai as genai

from dotenv import load_dotenv
import os

genai.configure(api_key=os.getenv('AI_KEY'))
model = genai.GenerativeModel("gemini-1.0-pro-latest")

def get_resp(loc):
    resp = model.generate_content(f"Can you tell me a bit more about {loc} in max 300-400 words?")
    return resp.text
    
