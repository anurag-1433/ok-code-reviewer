import requests

GITHUB_API = "https://api.github.com"

def get_pr(owner, repo, pr_number, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def get_pr_files(owner, repo, pr_number, token):
    headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "ai-code-reviewer",
}


    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def post_pr_comment(owner, repo, pr_number, token, body):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-code-reviewer",
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    res = requests.post(url, headers=headers, json={"body": body})
    res.raise_for_status()

def find_existing_ai_comment(owner, repo, pr_number, token, bot_name):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-code-reviewer",
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    for comment in res.json():
        user = comment.get("user", {})
        if user.get("login") == bot_name:
            return comment["id"]

    return None


def update_pr_comment(owner, repo, comment_id, token, body):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-code-reviewer",
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    res = requests.patch(url, headers=headers, json={"body": body})
    res.raise_for_status()


