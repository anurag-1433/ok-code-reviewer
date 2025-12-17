import os
from dotenv import load_dotenv
from app.github.auth import get_installation_token
from app.github.client import get_pr_files
from app.core.diff_parser import parse_pr_files

load_dotenv()

OWNER = "anurag-1433"
REPO = "test-repo"
PR_NUMBER = 1  # existing PR

token = get_installation_token(
    os.getenv("GITHUB_APP_ID"),
    os.getenv("GITHUB_INSTALLATION_ID"),
    os.getenv("GITHUB_PRIVATE_KEY_PATH"),
)

files = get_pr_files(OWNER, REPO, PR_NUMBER, token)
parsed = parse_pr_files(files)

for item in parsed:
    print(item["file"])
    print(item["patch"])
    print("-" * 40)
