import os
import json
from typing import Any
from core.crypto import encrypt_blob, decrypt_blob, generate_salt

VAULT_FILE = "vault.json"


def _load_vault_file() -> dict[str, Any]:
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_vault_file(data: dict[str, Any]) -> None:
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def list_users() -> list[str]:
    return list(_load_vault_file().keys())


def create_user(username: str, master_password: str) -> None:
    data = _load_vault_file()
    if username in data:
        raise ValueError(f"User '{username}' already exists.")

    empty_vault: dict[str, Any] = {}
    salt = generate_salt()
    encrypted_blob = encrypt_blob(empty_vault, master_password, salt)

    data[username] = {
        "salt": salt.hex(),
        "vault_data": encrypted_blob
    }
    _save_vault_file(data)


def load_user_vault(username: str, master_password: str) -> dict[str, Any]:
    data = _load_vault_file()
    if username not in data:
        raise ValueError(f"User '{username}' does not exist.")

    salt = bytes.fromhex(data[username]["salt"])
    encrypted_blob = data[username]["vault_data"]
    decrypted_vault = decrypt_blob(encrypted_blob, master_password, salt)

    if not isinstance(decrypted_vault, dict):
        raise ValueError("Decrypted vault is not a valid dictionary.")

    return decrypted_vault


def save_user_vault(username: str, master_password: str, vault_data: dict[str, Any]) -> None:
    data = _load_vault_file()
    if username not in data:
        raise ValueError(f"User '{username}' does not exist.")

    salt = bytes.fromhex(data[username]["salt"])
    encrypted_blob = encrypt_blob(vault_data, master_password, salt)

    data[username]["vault_data"] = encrypted_blob
    _save_vault_file(data)
