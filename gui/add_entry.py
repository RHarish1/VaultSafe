from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from core.crypto import encrypt_entry
from core.vault_io import load_vault, save_vault

class AddEntryWidget(QWidget):
    def __init__(self, parent=None, on_back=None):
        super().__init__(parent)
        self.on_back = on_back

        self.setMinimumWidth(500)
        self.setStyleSheet("background: #f4f7fa;")

        # === Layout Setup ===
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        label_style = "font-weight: bold; font-size: 15px; color: #185a9d;"

        # === Website URL ===
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Website URL (e.g., github.com)")
        self.url_input.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Website URL:", label_style), self.url_input)

        # === Username ===
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Username:", label_style), self.username_input)

        # === Password ===
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Password:", label_style), self.password_input)

        # === Master Password ===
        self.master_input = QLineEdit()
        self.master_input.setPlaceholderText("Master Password (never stored)")
        self.master_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.master_input.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Master Password:", label_style), self.master_input)

        # === Buttons ===
        button_layout = QVBoxLayout()
        self.save_btn = QPushButton("💾 Save Entry")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("font-size: 16px; font-weight: 500; border-radius: 8px; background: #43cea2; color: white;")
        self.save_btn.clicked.connect(self.save_entry)
        button_layout.addWidget(self.save_btn)

        if self.on_back:
            self.back_btn = QPushButton("← Back")
            self.back_btn.setMinimumHeight(40)
            self.back_btn.setStyleSheet("font-size: 15px; border-radius: 8px; background: #185a9d; color: white;")
            self.back_btn.clicked.connect(self.on_back)
            button_layout.addWidget(self.back_btn)

        # === Final Layout ===
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(main_layout)

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        return label

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
            vault[url] = {"salt": salt, "iv": iv, "ciphertext": ciphertext}
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
