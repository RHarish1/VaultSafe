from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from gui.add_entry import AddEntryWidget
from gui.view_entry import ViewEntryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultSafe - Offline Password Manager")
        self.setMinimumSize(800, 500)
        self.setup_ui()

    def setup_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # === Header ===
        self.header = QLabel("\U0001f510 VaultSafe - Offline Password Manager")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFixedHeight(60)
        self.main_layout.addWidget(self.header)

        # === Body Layout ===
        self.body_layout = QHBoxLayout()
        self.main_layout.addLayout(self.body_layout)

        # === Sidebar ===
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        self.sidebar.setSpacing(8)
        add_icon = QIcon("icons/add.png")
        view_icon = QIcon("icons/view.png")
        add_item = QListWidgetItem(add_icon, "  Add New Entry")
        add_item.setSizeHint(QtCore.QSize(200, 48))
        view_item = QListWidgetItem(view_icon, "  View Stored Entry")
        view_item.setSizeHint(QtCore.QSize(200, 48))
        self.sidebar.addItem(add_item)
        self.sidebar.addItem(view_item)
        self.sidebar.clicked.connect(self.handle_sidebar_click)

        # Sidebar layout with dark mode button at bottom
        self.body_layout.addWidget(self.sidebar)

        # === Content Area Wrapper ===
        self.content_wrapper = QWidget()
        self.content_wrapper_layout = QVBoxLayout(self.content_wrapper)
        self.content_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_wrapper.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f9f9f9, stop:1 #e6f2e6);")
        self.body_layout.addWidget(self.content_wrapper)

        # === Content Frame ===
        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        self.content_frame.setMaximumWidth(800)
        self.content_frame.setMinimumWidth(600)
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(20, 10, 20, 10)
        self.content_layout.setSpacing(10)
        self.content_wrapper_layout.addWidget(self.content_frame)

        # === Footer ===
        self.footer = QLabel("VaultSafe v1.0 | Secure Offline Password Manager")
        self.footer.setObjectName("FooterLabel")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer.setFixedHeight(36)
        self.main_layout.addWidget(self.footer)

        # Load default view
        self.show_home()

        # === Styles ===
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Roboto', 'Sans-Serif';
                background-color: #f4f7fa;
            }
            #HeaderLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 18px 0 18px 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #43cea2, stop:1 #185a9d);
                color: white;
                border-bottom: 2px solid #e0e0e0;
                letter-spacing: 1px;
            }
            #FooterLabel {
                color: #888;
                font-size: 12px;
                padding: 10px;
                background: #f4f4f4;
                border-top: 1px solid #e0e0e0;
            }
            QListWidget#Sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e0eafc, stop:1 #cfdef3);
                border-right: 2px solid #b2bec3;
                font-size: 16px;
                color: #222;
                outline: none;
                padding-top: 18px;
            }
            QListWidget#Sidebar::item {
                padding: 12px 18px;
                margin: 8px 10px;
                border-radius: 10px;
                font-size: 16px;
                min-height: 40px;
            }
            QListWidget#Sidebar::item:hover {
                background: #b2bec3;
                color: #fff;
            }
            QListWidget#Sidebar::item:selected {
                background: #43cea2;
                color: white;
                font-weight: bold;
                outline: none;
            }
            QFrame#ContentFrame {
                background: #fff;
                border: 1.5px solid #b2bec3;
                border-radius: 16px;
                padding: 18px;
                margin: 18px;
                color: #222;
            }
            QLineEdit {
                color: #222;
                background: #f9f9f9;
                border: 1.5px solid #b2bec3;
                border-radius: 8px;
                padding: 8px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #43cea2;
                background: #e0f7fa;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #43cea2, stop:1 #185a9d);
                color: white;
                font-size: 15px;
                border-radius: 8px;
                padding: 8px 0;
                font-weight: 500;
                margin-top: 6px;
                min-width: 120px;
                min-height: 36px;
            }
            QPushButton:hover {
                background: #185a9d;
            }
            QLabel {
                color: #222;
                font-size: 14px;
                padding-left: 2px;
            }
            QComboBox {
                color: #222;
                background: #f9f9f9;
                border: 1.5px solid #b2bec3;
                border-radius: 8px;
                padding: 7px;
                font-size: 14px;
                min-height: 32px;
                min-width: 320px;
                margin-bottom: 8px;
            }
            QComboBox QAbstractItemView {
                color: #222;
                background: #fff;
                selection-background-color: #e0f2e9;
                border: 1.5px solid #b2bec3;
                padding: 6px;
                outline: none;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1.5px solid #b2bec3;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background: #f4f7fa;
            }
            QComboBox::down-arrow {
                width: 16px;
                height: 16px;
            }
        """)

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_home(self):
        self.clear_content()
        welcome = QLabel("""
            <div style='text-align:center;'>
                <span style='font-size:40px;'>&#128273;</span><br>
                <span style='font-size:20px;font-weight:bold;'>Welcome to VaultSafe!</span><br>
                <span style='font-size:15px;'>Select an option from the left to get started.</span>
            </div>
        """)
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 16px; margin-top: 30px;")
        self.content_layout.addWidget(welcome)

    def show_add_entry(self):
        self.clear_content()
        self.content_layout.addWidget(AddEntryWidget(on_back=self.show_home))

    def show_view_entry(self):
        self.clear_content()
        self.content_layout.addWidget(ViewEntryWidget(on_back=self.show_home))

    def handle_sidebar_click(self, index):
        if index.row() == 0:
            self.show_add_entry()
        elif index.row() == 1:
            self.show_view_entry()