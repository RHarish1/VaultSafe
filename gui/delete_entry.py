from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QComboBox,
    QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from core.vault_io import save_user_vault


class DeleteEntryWidget(QWidget):
    def __init__(self, username: str, master_password: str, vault_data: dict, on_back=None):
        super().__init__()
        self.username = username
        self.master_password = master_password
        self.vault_data = vault_data
        self.on_back = on_back

        self.setMinimumWidth(500)
        self.setStyleSheet("background: #f4f7fa;")

        self.site_combo = QComboBox()
        self.site_combo.setMinimumHeight(36)
        self.site_combo.addItems(sorted(self.vault_data.keys()))
        self.site_combo.currentTextChanged.connect(self.populate_usernames)

        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(36)

        self.populate_usernames(self.site_combo.currentText())

        self.delete_btn = QPushButton("🗑️ Delete Entry")
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setStyleSheet("font-size: 15px; background: #c0392b; color: white; border-radius: 8px;")
        self.delete_btn.clicked.connect(self.delete_entry)

        self.back_btn = QPushButton("← Back")
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setStyleSheet("font-size: 15px; background: #888; color: white; border-radius: 8px;")
        if self.on_back:
            self.back_btn.clicked.connect(self.on_back)

        form_layout = QFormLayout()
        label_style = "font-weight: bold; font-size: 15px; color: #185a9d;"
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        form_layout.addRow(self._styled_label("Select Website:", label_style), self.site_combo)
        form_layout.addRow(self._styled_label("Select Username:", label_style), self.user_combo)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)

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

    def populate_usernames(self, site):
        self.user_combo.clear()
        if site in self.vault_data:
            self.user_combo.addItems(sorted(self.vault_data[site].keys()))

    def delete_entry(self):
        site = self.site_combo.currentText()
        user = self.user_combo.currentText()

        if not site or not user:
            QMessageBox.warning(self, "Error", "Select both site and username to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the entry for:\n\nWebsite: {site}\nUsername: {user}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            del self.vault_data[site][user]
            if not self.vault_data[site]:
                del self.vault_data[site]

            save_user_vault(self.username, self.master_password, self.vault_data)

            QMessageBox.information(self, "Deleted", f"Entry for {user} at {site} deleted.")

            self.site_combo.clear()
            self.site_combo.addItems(sorted(self.vault_data.keys()))
            self.populate_usernames(self.site_combo.currentText())

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete entry.\n{str(e)}")
