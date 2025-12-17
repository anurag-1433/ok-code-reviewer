import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# IMPORTANT: Gemini uses GOOGLE_API_KEY (official)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are a senior software engineer reviewing a pull request.

Rules:
- Review only the provided diff.
- Do not assume unseen code.
- Be concise and high-signal.
- Output STRICT JSON only.

Return format:
{
  "summary": "...",
  "comments": [
    {
      "file": "...",
      "severity": "blocker | warning | suggestion",
      "message": "..."
    }
  ]
}
"""

def review_code(context: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            SYSTEM_PROMPT,
            context
        ],
    )
    return response.text
