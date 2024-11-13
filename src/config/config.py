import google.generativeai as genai
import os
GEMINI_API_KEY = "put_your_api_key_here"

genai.configure(api_key=GEMINI_API_KEY)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

model = genai.GenerativeModel(model_name="gemini-1.5-flash")



