# vaultsafe/main.py

import sys
from PyQt6.QtWidgets import QApplication
from gui.user_selection import UserSelectionWidget
from gui.password_prompt import PasswordPromptWidget
from gui.main_window import MainWindow


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.username = None
        self.master_password = None
        self.vault_data = None

        self.user_selection = UserSelectionWidget(self.handle_user_selected)
        self.user_selection.show()

    def handle_user_selected(self, username):
        self.username = username
        self.user_selection.close()

        self.password_prompt = PasswordPromptWidget(username, self.handle_authenticated)
        self.password_prompt.show()

    def handle_authenticated(self, username, master_password, vault_data):
        self.username = username
        self.master_password = master_password
        self.vault_data = vault_data

        self.password_prompt.close()

        self.main_window = MainWindow(
            username=username,
            master_password=master_password,
            vault_data=vault_data
        )
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
