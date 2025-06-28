from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)
from gui.add_entry import AddEntryWidget
from gui.view_entry import ViewEntryWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultSafe - Offline Password Manager")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.label = QLabel("Welcome to VaultSafe!")
        self.add_btn = QPushButton("Add New Entry")
        self.view_btn = QPushButton("View Stored Entry")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.view_btn)

        self.add_btn.clicked.connect(self.show_add_entry)
        self.view_btn.clicked.connect(self.show_view_entry)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def show_add_entry(self):
        self.clear_layout()
        self.layout.addWidget(AddEntryWidget(self))

    def show_view_entry(self):
        self.clear_layout()
        self.layout.addWidget(ViewEntryWidget(self))
