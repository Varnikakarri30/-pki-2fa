#!/usr/bin/env python3
import subprocess, base64
from app.crypto_utils import load_private_key, load_public_key, sign_commit_hash, encrypt_with_instructor_public

commit_hash = subprocess.check_output(["git", "log", "-1", "--format=%H"]).decode().strip()
priv = load_private_key("student_private.pem")
sig = sign_commit_hash(commit_hash, priv)
instr_pub = load_public_key("instructor_public.pem")
enc = encrypt_with_instructor_public(sig, instr_pub)
b64 = base64.b64encode(enc).decode('utf-8')
print("Commit Hash:", commit_hash)
print("Encrypted Signature (base64, single line):")
print(b64)
