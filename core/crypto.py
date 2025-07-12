import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# === Constants ===
PBKDF2_ITERATIONS = 200_000
KEY_LENGTH = 32       # 256-bit AES key
SALT_LENGTH = 16      # 128-bit salt
IV_LENGTH = 12        # 96-bit IV (recommended for AES-GCM)


# === Key Derivation ===
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode())


# === Salt Generator ===
def generate_salt() -> bytes:
    return os.urandom(SALT_LENGTH)


# === Encrypt Vault Blob (full vault as one encrypted string) ===
def encrypt_blob(data: dict, master_password: str, salt: bytes) -> str:
    key = derive_key(master_password, salt)
    iv = os.urandom(IV_LENGTH)
    aesgcm = AESGCM(key)

    plaintext = json.dumps(data).encode("utf-8")
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    blob = {
        "iv": iv.hex(),
        "ciphertext": ciphertext.hex()
    }

    blob_json = json.dumps(blob).encode("utf-8")
    return base64.b64encode(blob_json).decode("utf-8")


# === Decrypt Vault Blob (full vault from encrypted string) ===
def decrypt_blob(encrypted_blob: str, master_password: str, salt: bytes) -> dict:
    try:
        blob_json = base64.b64decode(encrypted_blob.encode("utf-8")).decode("utf-8")
        blob = json.loads(blob_json)

        iv = bytes.fromhex(blob["iv"])
        ciphertext = bytes.fromhex(blob["ciphertext"])

        key = derive_key(master_password, salt)
        aesgcm = AESGCM(key)

        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return json.loads(plaintext.decode("utf-8"))
    except Exception:
        return {"username": "???", "password": "???"}


# === Per-Entry Encryption ===
def encrypt_entry(master_password: str, entry_data: dict) -> tuple:
    salt = generate_salt()
    key = derive_key(master_password, salt)
    iv = os.urandom(IV_LENGTH)
    aesgcm = AESGCM(key)

    plaintext = json.dumps(entry_data).encode("utf-8")
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return salt.hex(), iv.hex(), ciphertext.hex()


# === Per-Entry Decryption ===
def decrypt_entry(master_password: str, salt_hex: str, iv_hex: str, ciphertext_hex: str) -> dict:
    try:
        salt = bytes.fromhex(salt_hex)
        iv = bytes.fromhex(iv_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)

        key = derive_key(master_password, salt)
        aesgcm = AESGCM(key)

        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return json.loads(plaintext.decode("utf-8"))
    except Exception:
        return {"username": "???", "password": "???"}
