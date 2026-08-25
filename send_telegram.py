import os
import sys

import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ.get("CHAT_ID", "")
STATUS = os.environ.get("JOB_STATUS", "")


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text[:4000]},
        timeout=30,
    )


def main():
    if not CHAT_ID:
        return
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            import json

            result = json.load(f)
    except Exception as e:
        send(f"SUDIM job failed before producing a result: {e} (status: {STATUS})")
        return
    if result.get("ok"):
        import json

        send(json.dumps(result["data"], ensure_ascii=False, indent=2))
    else:
        msg = f"SUDIM lookup failed: {result.get('error')}"
        if result.get("log"):
            msg += "\n" + result["log"][:800]
        send(msg)


if __name__ == "__main__":
    main()
