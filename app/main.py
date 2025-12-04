# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

from totp_utils import generate_totp, verify_totp
from crypto_utils import load_private_key, decrypt_seed_base64

DATA_PATH = Path("/data")
SEED_FILE = DATA_PATH / "seed.txt"
PRIVATE_KEY_PATH = Path("/app/student_private.pem")  # inside container

app = FastAPI()

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed(req: DecryptRequest):
    try:
        private_key = load_private_key(str(PRIVATE_KEY_PATH))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Private key load failed: {str(e)}"})

    try:
        hex_seed = decrypt_seed_base64(req.encrypted_seed, private_key)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})

    # Validate seed is 64 hex chars
    if not (len(hex_seed) == 64 and all(c in "0123456789abcdef" for c in hex_seed.lower())):
        raise HTTPException(status_code=500, detail={"error": "Invalid seed format after decryption"})

    DATA_PATH.mkdir(parents=True, exist_ok=True)
    (SEED_FILE).write_text(hex_seed)
    os.chmod(SEED_FILE, 0o600)
    return {"status": "ok"}

@app.get("/generate-2fa")
async def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    hex_seed = SEED_FILE.read_text().strip()
    try:
        code, rem = generate_totp(hex_seed)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "TOTP generation failed"})
    return {"code": code, "valid_for": rem}

@app.post("/verify-2fa")
async def verify_2fa(req: VerifyRequest):
    code = req.code
    if code is None:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    hex_seed = SEED_FILE.read_text().strip()
    try:
        valid = verify_totp(hex_seed, code, window=1)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Verification error"})
    return {"valid": valid}
