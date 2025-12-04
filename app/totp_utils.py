import base64
import pyotp
import time
from typing import Tuple

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    b32 = base64.b32encode(seed_bytes).decode('utf-8')
    return b32

def generate_totp(hex_seed: str) -> Tuple[str,int]:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30)
    code = totp.now()
    rem = 30 - (int(time.time()) % 30)
    return code, rem

def verify_totp(hex_seed: str, code: str, window: int = 1) -> bool:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30)
    return totp.verify(code, valid_window=window)
