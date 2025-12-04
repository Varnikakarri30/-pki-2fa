#!/usr/bin/env python3
from pathlib import Path
from app.totp_utils import generate_totp
from datetime import datetime, timezone
import os

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
        import sys
        print(str(e), file=sys.stderr)

if __name__ == "__main__":
    main()
