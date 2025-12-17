import os
import requests
from dotenv import load_dotenv
from app.github.auth import get_installation_token

load_dotenv()

token = get_installation_token(
    os.getenv("GITHUB_APP_ID"),
    os.getenv("GITHUB_INSTALLATION_ID"),
    os.getenv("GITHUB_PRIVATE_KEY_PATH"),
)

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
}

res = requests.get("https://api.github.com/installation/repositories", headers=headers)
print(res.status_code)
print(res.json())
