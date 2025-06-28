from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
)
from gui.add_entry import AddEntryWidget
from gui.view_entry import ViewEntryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultSafe - Offline Password Manager")
        self.setMinimumSize(400, 300)

        # Main container widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Layout to hold both header and content
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Header (static)
        self.label = QLabel("🔐 Welcome to VaultSafe!")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_btn = QPushButton("➕ Add New Entry")
        self.view_btn = QPushButton("📄 View Stored Entry")

        for btn in (self.add_btn, self.view_btn):
            btn.setStyleSheet("padding: 8px; font-size: 14px;")

        self.add_btn.clicked.connect(self.show_add_entry)
        self.view_btn.clicked.connect(self.show_view_entry)

        # Static header
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.add_btn)
        self.main_layout.addWidget(self.view_btn)

        # Content area (dynamic)
        self.content_frame = QFrame()
        self.content_layout = QVBoxLayout()
        self.content_frame.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_frame)

        # Initially load home screen
        self.show_home()

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_home(self):
        self.clear_content()
        self.label.setText("🔐 Welcome to VaultSafe!")
        self.add_btn.show()
        self.view_btn.show()

    def show_add_entry(self):
        self.clear_content()
        self.label.setText("➕ Add New Entry")
        self.add_btn.hide()
        self.view_btn.hide()
        self.content_layout.addWidget(AddEntryWidget(on_back=self.show_home))

    def show_view_entry(self):
        self.clear_content()
        self.label.setText("📄 View Stored Entry")
        self.add_btn.hide()
        self.view_btn.hide()
        self.content_layout.addWidget(ViewEntryWidget(on_back=self.show_home))
