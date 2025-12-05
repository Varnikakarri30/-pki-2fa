#!/usr/bin/env python3
from pathlib import Path
import os
from datetime import datetime, timezone

# Try both import styles so it works inside container and during local tests
try:
    # When running with PYTHONPATH=/app or when package installed as 'app'
    from app.totp_utils import generate_totp
except Exception:
    # When running from /app where totp_utils.py is top-level
    from totp_utils import generate_totp

SEED_FILE = Path("/data/seed.txt")
OUT = Path("/cron/last_code.txt")

def main():
    try:
        if not SEED_FILE.exists():
            print("Seed file not found", flush=True)
            return
        hex_seed = SEED_FILE.read_text().strip()
        code, _ = generate_totp(hex_seed)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        line = f"{ts} - 2FA Code: {code}\n"
        os.makedirs("/cron", exist_ok=True)
        with open(OUT, "a") as f:
            f.write(line)
    except Exception as e:
        import sys, traceback
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    main()
