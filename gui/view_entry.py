from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QVBoxLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QGuiApplication

from core.vault_io import load_vault, save_vault
from core.crypto import decrypt_entry, encrypt_entry


class ViewEntryWidget(QWidget):
    def __init__(self, parent=None, on_back=None):
        super().__init__(parent)
        self.on_back = on_back
        self.vault = load_vault()

        # === Layout Setup ===
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        label_style = "font-weight: bold; font-size: 15px; color: #185a9d;"

        # === Site ComboBox ===
        self.site_combo = QComboBox()
        self.site_combo.setMinimumHeight(36)
        self.site_combo.addItems(sorted(self.vault.keys()))
        form_layout.addRow(self._styled_label("Select Website:", label_style), self.site_combo)

        # === Master Password Input ===
        self.master_input = QLineEdit()
        self.master_input.setPlaceholderText("Master Password")
        self.master_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.master_input.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Master Password:", label_style), self.master_input)

        # === Username Display ===
        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        self.username_display.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Username:", label_style), self.username_display)

        # === Password Display ===
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setMinimumHeight(36)
        form_layout.addRow(self._styled_label("Password:", label_style), self.password_display)

        # === Button Area ===
        self.reveal_btn = QPushButton("🔍 Reveal Credentials")
        self.reveal_btn.setMinimumHeight(40)
        self.reveal_btn.setStyleSheet("font-size: 16px; font-weight: 500; border-radius: 8px; background: #43cea2; color: white;")
        self.copy_btn = QPushButton("📋 Copy Password")
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.setStyleSheet("font-size: 15px; border-radius: 8px; background: #185a9d; color: white;")
        self.update_btn = QPushButton("✏️ Update Entry")
        self.update_btn.setMinimumHeight(40)
        self.update_btn.setStyleSheet("font-size: 15px; border-radius: 8px; background: #f39c12; color: white;")
        self.update_btn.setEnabled(False)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.reveal_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.update_btn)

        if self.on_back:
            self.back_btn = QPushButton("← Back")
            self.back_btn.setMinimumHeight(40)
            self.back_btn.setStyleSheet("font-size: 15px; border-radius: 8px; background: #888; color: white;")
            btn_layout.addWidget(self.back_btn)

        # === Set Up Actions ===
        self.reveal_btn.clicked.connect(self.reveal_entry)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.update_btn.clicked.connect(self.update_entry)
        if self.on_back:
            self.back_btn.clicked.connect(self.on_back)

        # === Final Layout ===
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(main_layout)

        self.setStyleSheet("background: #f4f7fa;")

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        return label

    def reveal_entry(self):
        site = self.site_combo.currentText()
        master = self.master_input.text().strip()

        if not site or not master:
            QMessageBox.warning(self, "Error", "Select a site and enter master password.")
            return

        try:
            record = self.vault[site]
            data = decrypt_entry(master, record["salt"], record["iv"], record["ciphertext"])
            self.username_display.setText(data.get("username", "???"))
            self.password_display.setText(data.get("password", "???"))
            self.username_display.setReadOnly(False)
            self.password_display.setReadOnly(False)
            self.update_btn.setEnabled(True)
            self._current_site = site
            self._current_master = master
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decrypt: {str(e)}")

    def copy_to_clipboard(self):
        QGuiApplication.clipboard().setText(self.password_display.text())
        QTimer.singleShot(10_000, lambda: QGuiApplication.clipboard().clear())
        QMessageBox.information(self, "Copied", "Password copied to clipboard (clears in 10s)")

    def update_entry(self):
        site = getattr(self, '_current_site', None)
        master = getattr(self, '_current_master', None)
        if not site or not master:
            QMessageBox.warning(self, "Error", "Reveal credentials first.")
            return
        username = self.username_display.text().strip()
        password = self.password_display.text().strip()
        if not (username and password):
            QMessageBox.warning(self, "Error", "Username and password cannot be empty.")
            return
        try:
            salt, iv, ciphertext = encrypt_entry(master, {"username": username, "password": password})
            self.vault[site] = {"salt": salt, "iv": iv, "ciphertext": ciphertext}
            save_vault(self.vault)
            QMessageBox.information(self, "Success", "Entry updated.")
            self.username_display.setReadOnly(True)
            self.password_display.setReadOnly(True)
            self.update_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update entry.\n{str(e)}")
