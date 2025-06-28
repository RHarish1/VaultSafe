from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QGuiApplication

from core.vault_io import load_vault
from core.crypto import decrypt_entry


class ViewEntryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vault = load_vault()

        layout = QVBoxLayout()

        self.site_combo = QComboBox()
        self.site_combo.addItems(sorted(self.vault.keys()))
        layout.addWidget(QLabel("Select Website:"))
        layout.addWidget(self.site_combo)

        self.master_input = QLineEdit()
        self.master_input.setPlaceholderText("Master Password")
        self.master_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Master Password:"))
        layout.addWidget(self.master_input)

        self.reveal_btn = QPushButton("Reveal Credentials")
        self.reveal_btn.clicked.connect(self.reveal_entry)
        layout.addWidget(self.reveal_btn)

        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_display)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_display)

        self.copy_btn = QPushButton("Copy Password")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_btn)

        self.setLayout(layout)

    def reveal_entry(self):
        site = self.site_combo.currentText()
        master = self.master_input.text()

        if not site or not master:
            QMessageBox.warning(self, "Error", "Select a site and enter master password.")
            return

        try:
            record = self.vault[site]
            data = decrypt_entry(master, record["salt"], record["iv"], record["ciphertext"])
            self.username_display.setText(data.get("username", "???"))
            self.password_display.setText(data.get("password", "???"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decrypt: {str(e)}")

    def copy_to_clipboard(self):
        text = self.password_display.text()
        QGuiApplication.clipboard().setText(text)

        # Auto-clear after 10 seconds
        QTimer.singleShot(10_000, lambda: QGuiApplication.clipboard().clear())
        QMessageBox.information(self, "Copied", "Password copied to clipboard (clears in 10s)")
