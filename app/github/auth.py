import jwt, time, requests
from pathlib import Path

def get_installation_token(app_id, installation_id, private_key_path):
    private_key = Path(private_key_path).read_text()

    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + 600,
        "iss": app_id,
    }

    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    res = requests.post(url, headers=headers)
    res.raise_for_status()

    return res.json()["token"]
