#!/usr/bin/env python3
import os
from datetime import datetime, timezone

# Try plain module import first, then package-style import as fallback,
# but do NOT print intermediate tracebacks (silent fallback).
generate_totp = None
try:
    from totp_utils import generate_totp  # preferred
except Exception:
    try:
        from app.totp_utils import generate_totp  # fallback
    except Exception:
        generate_totp = None

if generate_totp is None:
    # If both imports failed, raise a concise error (no long traceback)
    raise ImportError("Could not import TOTP generator (totp_utils or app.totp_utils)")

DATA_FILE = "/data/seed.txt"
OUT_FILE = "/cron/last_code.txt"

def main():
    try:
        if not os.path.exists(DATA_FILE):
            # Keep the log small and explicit
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
        # Print a short message to stderr (no traceback)
        import sys
        print("Cron job failed: " + str(sys.exc_info()[1]), file=sys.stderr)

if __name__ == "__main__":
    main()
