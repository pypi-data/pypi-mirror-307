import os
import json
import bcrypt
import logging
from cryptography.fernet import Fernet
from dart_app.config.logging_config import DBLogHandler
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(DBLogHandler())


class SetupWindow(QMainWindow):
    def __init__(self, on_setup_complete):
        super().__init__()
        self.on_setup_complete = on_setup_complete
        self.setWindowTitle("DART Initial Setup")
        self.setFixedSize(300, 200)

        self.setup_ui()

    def setup_ui(self):
        # Create widgets
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        setup_button = QPushButton("Create Admin Account", self)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Admin Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Admin Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(setup_button)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Button action
        setup_button.clicked.connect(self.create_admin_account)

    def create_admin_account(self):
        username = self.username_input.text()
        password = self.password_input.text().encode("utf-8")

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

        # Prepare user data
        user_data = {
            "users": [{"username": username, "password": hashed_password, "role": "admin"}]
        }

        # Encrypt and save the user data
        key = os.getenv("DART_KEY")
        if not key:
            QMessageBox.critical(self, "Error", "Encryption key not found!")
            return

        cipher = Fernet(key.encode())
        json_data = json.dumps(user_data).encode("utf-8")
        encrypted_data = cipher.encrypt(json_data)

        with open("encrypted_users.json", "wb") as file:
            file.write(encrypted_data)

        QMessageBox.information(self, "Setup Complete", "Admin account created successfully!")
        self.close()
        self.on_setup_complete()
