from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

from app.github.auth import get_installation_token
from app.github.client import (
    get_pr_files,
    post_pr_comment,
    find_existing_ai_comment,
    update_pr_comment,
)
from app.core.diff_parser import parse_pr_files
from app.core.context_builder import build_context
from app.ai.reviewer import review_code

load_dotenv()

app = FastAPI()


@app.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()

    # Only handle PR open / update events
    if payload.get("action") not in ["opened", "synchronize"]:
        return {"status": "ignored"}

    # IMPORTANT: respond immediately to GitHub
    process_pr(payload)

    return {"status": "accepted"}


def process_pr(payload: dict):
    try:
        pr = payload["pull_request"]
        repo = payload["repository"]
        installation_id = payload["installation"]["id"]

        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        pr_number = pr["number"]

        token = get_installation_token(
            os.getenv("GITHUB_APP_ID"),
            installation_id,
            os.getenv("GITHUB_PRIVATE_KEY_PATH"),
        )

        files = get_pr_files(owner, repo_name, pr_number, token)
        parsed = parse_pr_files(files)
        context = build_context(parsed)

        # AI review (resilient)
        try:
            review = review_code(context)
        except Exception as e:
            print("AI error:", e)
            review = (
                "⚠️ **AI review temporarily unavailable**\n\n"
                "The model is currently overloaded. "
                "This PR will be reviewed again on the next update."
            )

        BOT_NAME = "ok-code-reviewer[bot]"
        comment_body = f"🤖 **AI Code Review**\n\n{review}"

        existing_comment_id = find_existing_ai_comment(
            owner,
            repo_name,
            pr_number,
            token,
            BOT_NAME,
        )

        if existing_comment_id:
            update_pr_comment(
                owner,
                repo_name,
                existing_comment_id,
                token,
                comment_body,
            )
        else:
            post_pr_comment(
                owner,
                repo_name,
                pr_number,
                token,
                comment_body,
            )

    except Exception as e:
        # NEVER crash the webhook
        print("Webhook processing error:", e)

if __name__ == "__main__":
    import uvicorn
    import os

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
    )
