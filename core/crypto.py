import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants
PBKDF2_ITERATIONS = 200_000  # increase for slower brute-force
KEY_LENGTH = 32              # 256-bit AES
SALT_LENGTH = 16
IV_LENGTH = 12               # Recommended for AES-GCM

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS
    )
    return kdf.derive(password.encode())

def encrypt_entry(master_password: str, data: dict) -> tuple[str, str, str]:
    salt = os.urandom(SALT_LENGTH)
    iv = os.urandom(IV_LENGTH)
    key = derive_key(master_password, salt)

    aesgcm = AESGCM(key)
    plaintext = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return (
        base64.b64encode(salt).decode(),
        base64.b64encode(iv).decode(),
        base64.b64encode(ciphertext).decode()
    )

def decrypt_entry(master_password: str, salt_b64: str, iv_b64: str, ciphertext_b64: str) -> dict:
    salt = base64.b64decode(salt_b64)
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return json.loads(plaintext.decode())
    except Exception:
        # Even if wrong password or tampered data — return random garbage
        return {"username": "???", "password": "???"}
