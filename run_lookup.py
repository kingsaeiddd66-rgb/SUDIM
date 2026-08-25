import json
import os
import shutil
import subprocess
import sys
import uuid

MESSENGERS = ["eitaa", "bale", "soroush", "shad", "igap", "rubika"]
SUDIM_CMD = os.getenv(
    "SUDIM_CMD",
    "python -m sudim --messenger {messenger} --phone {phone} --profile {profile} --output {output}",
)
TIMEOUT = int(os.getenv("JOB_TIMEOUT_SECONDS", "780"))


def clean_locks(profile_dir):
    for name in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
        p = os.path.join(profile_dir, name)
        if os.path.lexists(p):
            os.remove(p)


def run_lookup(messenger, phone, job_id):
    profile = os.path.join("/tmp", f"sudim_profile_{job_id}")
    output = "/tmp/result.json"
    os.makedirs(profile, exist_ok=True)

    src = os.path.join("sessions", messenger)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(profile, "Default"), dirs_exist_ok=True)

    clean_locks(profile)

    cmd = SUDIM_CMD.format(
        messenger=messenger, phone=phone, profile=profile, output=output
    )
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        tail = (proc.stdout or "") + "\n" + (proc.stderr or "")
        if os.path.exists(output):
            with open(output, encoding="utf-8") as f:
                return {"ok": True, "data": json.load(f)}
        return {
            "ok": False,
            "error": "no_result_file",
            "log": tail[-1500:],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout_after_{TIMEOUT}s"}
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def main():
    messenger, phone, job_id = sys.argv[1], sys.argv[2], sys.argv[3]
    if messenger not in MESSENGERS:
        result = {"ok": False, "error": f"unknown messenger {messenger}"}
    else:
        try:
            result = run_lookup(messenger, phone, job_id)
        except Exception as e:
            result = {"ok": False, "error": str(e)}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    print(json.dumps(result, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
