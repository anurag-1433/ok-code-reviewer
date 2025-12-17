import os
from dotenv import load_dotenv
from app.github.auth import get_installation_token

load_dotenv()

token = get_installation_token(
    os.getenv("GITHUB_APP_ID"),
    os.getenv("GITHUB_INSTALLATION_ID"),
    os.getenv("GITHUB_PRIVATE_KEY_PATH"),
)

print("Token generated:", token[:10], "...")
