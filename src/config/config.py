# !pip install python-dotenv
#set GOOGLE_APPLICATION_CREDENTIALS=D:\path\to\your\service-account-file.json


import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
     print("API key not found in environment. Please ensure GEMINI_API_KEY is set.")
     exit(1)

# Configure the API with the key
genai.configure(api_key=GEMINI_API_KEY)

# You can now use the key for API requests
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
########################################################################################
# Set the URL and headers
# url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# headers = {
#     'Content-Type': 'application/json'
# }

# # Set the payload (data)
# payload = {
#     "contents": [{
#         "parts": [{
#             "text": "What is square root of 64?"
#         }]
#     }]
# }

# # Send the POST request
# response = requests.post(url, headers=headers, params={'key': GEMINI_API_KEY}, json=payload)

# # Check the response
# if response.status_code == 200:
#     print("Generated content:", response.json())
# else:
#     print("Error:", response.status_code, response.text)

