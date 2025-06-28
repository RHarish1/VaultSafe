import os
import json

VAULT_FILE = "vault.json"

def load_vault() -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Vault corrupted or unreadable
        return {}

def save_vault(vault: dict) -> None:
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=2)
