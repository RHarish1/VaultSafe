from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from core.crypto import encrypt_entry
from core.vault_io import save_user_vault


class AddEntryWidget(QWidget):
    def __init__(
        self,
        username: str,
        master_password: str,
        vault_data: dict,
        on_back=None,
        editing: bool = False,
        edit_website: Optional[str] = None,
        edit_username: Optional[str] = None,
        edit_password: Optional[str] = None
    ):
        super().__init__()
        self.username = username
        self.master_password = master_password
        self.vault_data = vault_data
        self.on_back = on_back
        self.editing = editing
        self.edit_website = edit_website
        self.edit_username = edit_username
        self.edit_password = edit_password

        self.setMinimumWidth(500)
        self.setStyleSheet("background: #f4f7fa;")
        self.setup_ui()

    def setup_ui(self):
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        label_style = "font-weight: bold; font-size: 15px; color: #185a9d;"

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Website URL (e.g., github.com)")
        self.url_input.setMinimumHeight(36)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(36)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(36)

        form_layout.addRow(self._styled_label("Website URL:", label_style), self.url_input)
        form_layout.addRow(self._styled_label("Username:", label_style), self.username_input)
        form_layout.addRow(self._styled_label("Password:", label_style), self.password_input)

        self.save_btn = QPushButton("💾 Save Entry" if not self.editing else "✏️ Update Entry")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("font-size: 16px; font-weight: 500; border-radius: 8px; background: #43cea2; color: white;")
        self.save_btn.clicked.connect(self.save_entry)

        self.back_btn = QPushButton("← Back")
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setStyleSheet("font-size: 15px; border-radius: 8px; background: #185a9d; color: white;")
        self.back_btn.clicked.connect(self.on_back)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.back_btn)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(main_layout)

        if self.editing:
            self.url_input.setText(self.edit_website or "")
            self.username_input.setText(self.edit_username or "")
            self.password_input.setText(self.edit_password or "")

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        return label

    def save_entry(self):
        website = self.url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not website or not username or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        try:
            # Get or create list for this website
            existing_entries = self.vault_data.get(website, [])

            if self.editing:
                # Overwrite the edited entry
                existing_entries = [
                    entry for entry in existing_entries
                    if not (entry.get("username") == self.edit_username)
                ]

            # Encrypt and append new entry
            salt, iv, ciphertext = encrypt_entry(self.master_password, {
                "username": username,
                "password": password
            })

            encrypted_entry = {
                "salt": salt,
                "iv": iv,
                "ciphertext": ciphertext
            }
            existing_entries.append(encrypted_entry)

            self.vault_data[website] = existing_entries

            # ✅ FIX: Correct save call
            save_user_vault(self.username, self.master_password, self.vault_data)

            QMessageBox.information(self, "Success", "Entry saved.")
            if self.on_back:
                self.on_back()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry.\n{str(e)}")
