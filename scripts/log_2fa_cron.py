#!/usr/bin/env python3
import os
from datetime import datetime, timezone

# Try the plain module name first because files are in /app as modules (not a package)
try:
    from totp_utils import generate_totp
except Exception:
    # Defensive fallback to package-style import if handler expects that
    try:
        from app.totp_utils import generate_totp
    except Exception:
        raise

DATA_FILE = "/data/seed.txt"
OUT_FILE = "/cron/last_code.txt"

def main():
    try:
        if not os.path.exists(DATA_FILE):
            print("Seed file not found", flush=True)
            return
        hex_seed = open(DATA_FILE, "r").read().strip()
        code, _ = generate_totp(hex_seed)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        line = f"{ts} - 2FA Code: {code}\n"
        os.makedirs("/cron", exist_ok=True)
        with open(OUT_FILE, "a") as f:
            f.write(line)
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
