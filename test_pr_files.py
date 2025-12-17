import os
from dotenv import load_dotenv
from app.github.auth import get_installation_token
from app.github.client import get_pr_files

load_dotenv()

OWNER = "anurag-1433"      # change if needed
REPO = "test-repo"         # change if needed
PR_NUMBER = 1              # put an existing PR number

token = get_installation_token(
    os.getenv("GITHUB_APP_ID"),
    os.getenv("GITHUB_INSTALLATION_ID"),
    os.getenv("GITHUB_PRIVATE_KEY_PATH"),
)

files = get_pr_files(OWNER, REPO, PR_NUMBER, token)

for f in files:
    print(f["filename"])
    print(f.get("patch"))
    print("-" * 40)
