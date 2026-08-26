import json
from pathlib import Path

result = {
    "ok": True,
    "data": {
        "status": "TEST_SUCCESS",
        "message": "GitHub Actions and Telegram are working correctly."
    }
}

Path("result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("result.json created successfully.")
print(json.dumps(result, ensure_ascii=False, indent=2))
