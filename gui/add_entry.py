from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from core.crypto import encrypt_entry
from core.vault_io import load_vault, save_vault


class AddEntryWidget(QWidget):
    def __init__(self, parent=None, on_back=None):
        super().__init__(parent)
        self.on_back = on_back

        self.setMinimumHeight(300)
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Website URL (e.g., github.com)")
        layout.addWidget(QLabel("Website URL:"))
        layout.addWidget(self.url_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.master_input = QLineEdit()
        self.master_input.setPlaceholderText("Master Password (never stored)")
        self.master_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Master Password:"))
        layout.addWidget(self.master_input)

        self.save_btn = QPushButton("Save Entry")
        self.save_btn.clicked.connect(self.save_entry)
        layout.addWidget(self.save_btn)

        if self.on_back:
            self.back_btn = QPushButton("← Back")
            self.back_btn.clicked.connect(self.handle_back)
            layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def save_entry(self):
        url = self.url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        master = self.master_input.text().strip()

        if not (url and username and password and master):
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        try:
            salt, iv, ciphertext = encrypt_entry(master, {
                "username": username,
                "password": password
            })

            vault = load_vault()
            vault[url] = {
                "salt": salt,
                "iv": iv,
                "ciphertext": ciphertext
            }
            save_vault(vault)

            QMessageBox.information(self, "Success", "Entry saved.")
            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry.\n{str(e)}")

    def clear_fields(self):
        self.url_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.master_input.clear()

    def handle_back(self):
        if self.on_back:
            self.on_back()
