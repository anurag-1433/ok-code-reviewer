import os
from dotenv import load_dotenv
from app.github.auth import get_installation_token
from app.github.client import post_pr_comment

load_dotenv()

OWNER = "anurag-1433"
REPO = "test-repo"
PR_NUMBER = 1  # use your real PR number

token = get_installation_token(
    os.getenv("GITHUB_APP_ID"),
    os.getenv("GITHUB_INSTALLATION_ID"),
    os.getenv("GITHUB_PRIVATE_KEY_PATH"),
)

body = """
🤖 **AI Code Review Summary**

A new file `demo` has been added with placeholder content.

Suggestions:
- Clarify the purpose of this file or remove it if temporary.
- Add a trailing newline for consistency.
"""

post_pr_comment(OWNER, REPO, PR_NUMBER, token, body)

print("Comment posted successfully.")
