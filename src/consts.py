from pathlib import Path
import os

BACKEND_DIR = os.environ.get("BACKEND_DIR", "./backend")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]
TOKEN_PATH = (Path(BACKEND_DIR) / "token.json").resolve()
CREDENTIALS_PATH = (Path(BACKEND_DIR) / "credentials.json").resolve()

EMAIL_SIGNATURE = os.environ.get("EMAIL_SIGNATURE", "")

FLOW_PORT = int(os.environ.get("FLOW_PORT", 5000))
