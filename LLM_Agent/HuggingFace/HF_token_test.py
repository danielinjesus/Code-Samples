from huggingface_hub import HfApi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get token from environment
token = os.getenv("HF_TOKEN")

# Create API instance
api = HfApi()

try:
    # Try to get user info - this will verify if the token is valid
    user_info = api.whoami(token=token)
    print("[SUCCESS] Token is valid!")
    print(f"Username: {user_info['name']}")
    print(f"Email: {user_info['email']}")
except Exception as e:
    print("[ERROR] Token is invalid or there's an error:")
    print(str(e))