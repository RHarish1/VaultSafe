# 🔐 VaultSafe — Offline, Zero-Trust Password Manager (Python + PyQt6)

> A fully offline, GUI-based password manager with no autofill, no network access, and no stored master key. Designed for absolute local security — even wrong master passwords yield decoy output.

## 🚀 Features

- ✅ No Internet Access — Runs completely offline. No sync. No server.
- ✅ No Autofill — No browser injection. User manually copies passwords.
- ✅ Multiple Accounts per Site — Store many credentials per domain.
- ✅ Strong Encryption — AES-256-GCM + PBKDF2-HMAC-SHA512 with per-entry salt.
- ✅ Zero-Trust Architecture — No password validation, no oracle — only the user knows what’s valid.
- ✅ Clipboard Auto-Clear — Clears passwords from clipboard after 10 seconds.
- ✅ Decoy Output on Wrong Password — Always returns plausible data, never reveals failure.
- ✅ White-Box Design — Minimal external dependencies, maximum transparency.
- ✅ Cross-Platform GUI — Intuitive PyQt6 interface (Windows, macOS, Linux).

## 📦 Tech Stack

- Python 3.11+
- PyQt6 — GUI
- cryptography — AES-GCM, PBKDF2-HMAC-SHA512
- PyInstaller *(optional)* — Create `.exe` or `.app` for offline use

## 🧠 How It Works

VaultSafe never stores your master password — instead:

1. You enter a master password to encrypt credentials.
2. It derives a per-entry AES-256-GCM key using:
   - PBKDF2-HMAC-SHA512
   - A 128-bit salt (stored with each record)
3. Even with the wrong password, decryption returns *something* — only the correct one yields usable credentials.
4. There is no password correctness signal — user judgment is the only oracle.

## 📁 Folder Structure

```plaintext
vaultsafe/
├── gui/
│   ├── main_window.py
│   ├── add_entry.py
│   └── view_entry.py
├── core/
│   ├── crypto.py
│   └── vault_io.py
├── vault.json           # Encrypted storage file
├── main.py              # Entry point
├── requirements.txt
└── README.md
```

## 🧪 Run Locally

```bash
pip install -r requirements.txt
python main.py
```

## 🛠️ Packaging (Optional)

Build a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile main.py
```

> Add `--windowed` to avoid terminal window on Windows.

## 🔐 Security Philosophy

- Zero-trust model — Only the user decides what’s correct.
- No central server, no cloud, no autofill.
- White-box transparency — Readable, auditable Python code.
- Side-channel safe — No signal from password correctness.
- Garbage output returned for all wrong passwords (looks real).

## 💡 Why It’s Different

| Feature                     | VaultSafe        | Bitwarden / 1Password    |
|----------------------------|------------------|---------------------------|
| Fully Offline              | ✅ Yes           | ❌ No (Cloud Required)    |
| No Autofill                | ✅ Yes           | ❌ Injects into Browser   |
| No Password Validation     | ✅ Yes           | ❌ Validates Master Key   |
| Open Source                | ✅ Fully Open    | ⚠️ Partially Closed       |
| Custom Encryption Per Entry| ✅ Yes           | ❌ Often Uniform Per Vault|

## 📚 License

MIT — use it, audit it, fork it.

## 🙋‍♂️ Author

**Harish Ramaswamy and Devang Bajpai @ Delhi Technological University**  
This project is part of a real-world security portfolio — built with ❤️ for usability, privacy, and zero-trust sanity.

## 🔗 Contribute / Feedback

Found an issue? Want to contribute?  
Open an issue or pull request on [GitHub](https://github.com/yourusername/vaultsafe-offline).
