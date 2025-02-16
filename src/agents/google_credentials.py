import os
from google.auth import load_credentials_from_file

def get_google_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set!")
    
    credentials, _ = load_credentials_from_file(credentials_path)
    return credentials
