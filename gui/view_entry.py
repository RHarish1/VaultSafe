from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QVBoxLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QGuiApplication
from core.crypto import decrypt_entry


class ViewEntryWidget(QWidget):
    def __init__(self, username, master_password, vault_data, on_back=None, on_edit_entry=None):
        super().__init__()
        self.username = username
        self.master_password = master_password
        self.vault_data = vault_data
        self.on_back = on_back
        self.on_edit_entry = on_edit_entry or (lambda **kwargs: None)

        self.selected_site = None
        self.selected_entry = None

        self.setMinimumWidth(500)
        self.setStyleSheet("background: #f4f7fa;")
        self._build_ui()

    def _build_ui(self):
        label_style = "font-weight: bold; font-size: 15px; color: #185a9d;"

        # === ComboBoxes ===
        self.site_combo = QComboBox()
        self.site_combo.setMinimumHeight(36)
        self.site_combo.addItems(sorted(self.vault_data.keys()))
        self.site_combo.currentIndexChanged.connect(self.populate_usernames)

        self.username_combo = QComboBox()
        self.username_combo.setMinimumHeight(36)

        # === Decrypted Output ===
        self.username_display = QLineEdit()
        self.username_display.setReadOnly(True)
        self.username_display.setMinimumHeight(36)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_display.setMinimumHeight(36)

        # === Buttons ===
        self.reveal_btn = QPushButton("🔍 Reveal")
        self.copy_btn = QPushButton("📋 Copy Password")
        self.edit_btn = QPushButton("✏️ Edit Entry")
        self.back_btn = QPushButton("← Back")

        for btn in [self.reveal_btn, self.copy_btn, self.edit_btn, self.back_btn]:
            btn.setMinimumHeight(40)

        self.edit_btn.setEnabled(False)

        # === Layout ===
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        form_layout.addRow(self._styled_label("Website:", label_style), self.site_combo)
        form_layout.addRow(self._styled_label("Username:", label_style), self.username_combo)
        form_layout.addRow(self._styled_label("Decrypted Username:", label_style), self.username_display)
        form_layout.addRow(self._styled_label("Decrypted Password:", label_style), self.password_display)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.reveal_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.back_btn)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch(1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(main_layout)

        self.reveal_btn.clicked.connect(self.reveal_entry)
        self.copy_btn.clicked.connect(self.copy_password)
        self.edit_btn.clicked.connect(self.edit_entry)
        if self.on_back:
            self.back_btn.clicked.connect(self.on_back)

        self.populate_usernames()

    def _styled_label(self, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        return label

    def populate_usernames(self):
        self.username_combo.clear()
        site = self.site_combo.currentText()
        if site and site in self.vault_data:
            entries = self.vault_data[site]
            for entry in entries:
                try:
                    decrypted = decrypt_entry(self.master_password, entry["salt"], entry["iv"], entry["ciphertext"])
                    self.username_combo.addItem(decrypted.get("username", "???"))
                except Exception:
                    self.username_combo.addItem("???")

    def reveal_entry(self):
        site = self.site_combo.currentText()
        selected_username = self.username_combo.currentText()

        for entry in self.vault_data.get(site, []):
            decrypted = decrypt_entry(self.master_password, entry["salt"], entry["iv"], entry["ciphertext"])
            if decrypted.get("username") == selected_username:
                self.username_display.setText(decrypted["username"])
                self.password_display.setText(decrypted["password"])
                self.selected_site = site
                self.selected_entry = decrypted
                self.edit_btn.setEnabled(True)
                return

        QMessageBox.warning(self, "Error", "Could not decrypt entry.")

    def copy_password(self):
        if  QGuiApplication.clipboard():
            QGuiApplication.clipboard().setText(self.password_display.text())
        QTimer.singleShot(10_000, lambda: QGuiApplication.clipboard().clear())
        QMessageBox.information(self, "Copied", "Password copied to clipboard. Will clear in 10 seconds.")

    def edit_entry(self):
        if not (self.selected_site and self.selected_entry):
            QMessageBox.warning(self, "Error", "Reveal an entry first.")
            return
        self.on_edit_entry(
            username=self.username,
            master_password=self.master_password,
            vault_data=self.vault_data,
            editing=True,
            edit_website=self.selected_site,
            edit_username=self.selected_entry["username"],
            edit_password=self.selected_entry["password"]
        )
