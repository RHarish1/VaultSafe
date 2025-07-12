from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout
)
from core.vault_io import list_users, create_user

class UserSelectionWidget(QWidget):
    def __init__(self, on_user_selected_callback):
        super().__init__()
        self.on_user_selected_callback = on_user_selected_callback

        self.setWindowTitle("VaultZero - Select or Add User")
        self.setFixedSize(400, 250)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel("Select Existing User:")
        self.user_dropdown = QComboBox()
        self.refresh_user_list()

        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(self.proceed_with_selected_user)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.user_dropdown)
        self.main_layout.addWidget(self.continue_button)

        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(QLabel("or"))

        # Add new user section
        self.new_user_input = QLineEdit()
        self.new_user_input.setPlaceholderText("Enter new username")

        self.add_user_button = QPushButton("Add New User")
        self.add_user_button.clicked.connect(self.create_new_user)

        new_user_layout = QHBoxLayout()
        new_user_layout.addWidget(self.new_user_input)
        new_user_layout.addWidget(self.add_user_button)

        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(new_user_layout)

    def refresh_user_list(self):
        self.user_dropdown.clear()
        users = list_users()
        self.user_dropdown.addItems(users)

    def proceed_with_selected_user(self):
        selected_user = self.user_dropdown.currentText()
        if not selected_user:
            QMessageBox.warning(self, "No User Selected", "Please select a user to continue.")
            return
        self.on_user_selected_callback(selected_user)

    def create_new_user(self):
        username = self.new_user_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Invalid Username", "Username cannot be empty.")
            return

        try:
            create_user(username, "placeholder")  # real password will be handled in next screen
            QMessageBox.information(self, "User Created", f"User '{username}' added.")
            self.refresh_user_list()
            self.new_user_input.clear()
        except ValueError as e:
            QMessageBox.warning(self, "User Exists", str(e))
