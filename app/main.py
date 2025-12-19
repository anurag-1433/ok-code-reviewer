from fastapi import FastAPI, Request
import os
import threading
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


# -------------------------
# Health check (REQUIRED for Render)
# -------------------------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}


# -------------------------
# GitHub Webhook
# -------------------------
@app.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()

    # Only PR open / update
    if payload.get("action") not in ["opened", "synchronize"]:
        return {"status": "ignored"}

    # Run in background thread (non-blocking)
    threading.Thread(target=process_pr, args=(payload,)).start()

    return {"status": "accepted"}


# -------------------------
# PR Processing Logic
# -------------------------
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

        try:
            review = review_code(context)
        except Exception as e:
            print("AI error:", e)
            review = (
                "⚠️ **AI review temporarily unavailable**\n\n"
                "The model is overloaded. The PR will be reviewed again on the next update."
            )

        bot_name = "ok-code-reviewer[bot]"
        comment_body = f"🤖 **AI Code Review**\n\n{review}"

        existing_comment_id = find_existing_ai_comment(
            owner, repo_name, pr_number, token, bot_name
        )

        if existing_comment_id:
            update_pr_comment(
                owner, repo_name, existing_comment_id, token, comment_body
            )
        else:
            post_pr_comment(
                owner, repo_name, pr_number, token, comment_body
            )

    except Exception as e:
        # Never crash webhook
        print("Webhook processing error:", e)


# -------------------------
# Local run (Render ignores this)
# -------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
    )
