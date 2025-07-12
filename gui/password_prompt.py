from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox
)
from core.vault_io import load_user_vault


class PasswordPromptWidget(QWidget):
    def __init__(self, username: str, on_authenticated_callback):
        super().__init__()
        self.username = username
        self.on_authenticated_callback = on_authenticated_callback

        self.setWindowTitle(f"VaultZero - Enter Password for '{username}'")
        self.setFixedSize(400, 200)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel(f"Enter master password for '{username}':")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.try_login)

        self.login_button = QPushButton("Unlock Vault")
        self.login_button.clicked.connect(self.try_login)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.password_input)
        self.main_layout.addWidget(self.login_button)

    def try_login(self):
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Empty Password", "Please enter a master password.")
            return

        try:
            vault_data = load_user_vault(self.username, password)

            # check if vault_data is valid (not corrupted or incorrect password)
            if isinstance(vault_data, dict) and "error" not in vault_data:
                self.on_authenticated_callback(self.username, password, vault_data)
            else:
                QMessageBox.critical(self, "Access Denied", "Incorrect password or vault corrupted.")
        except Exception as e:
            QMessageBox.critical(self, "Access Failed", f"Could not open vault.\n\n{str(e)}")
