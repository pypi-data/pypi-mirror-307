import os
import bcrypt
import json
import logging
from dart_app.config.logging_config import DBLogHandler
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DBLogHandler())


class LoginWindow(QMainWindow):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("DART Login")
        self.setFixedSize(500, 250)
        logger.info("Login window initialized")

        self.setup_ui()

    def setup_ui(self):
        """Sets up the login UI."""

        # Main layout for the window
        main_layout = QVBoxLayout()

        # DART logo setup
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("resources/dart_logo.svg")  # Replace with actual path to logo
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Form layout for aligned labels and input fields
        form_layout = QFormLayout()

        # Username and Password fields
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("User Name:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        main_layout.addLayout(form_layout)

        # Buttons layout for Login and Close
        buttons_layout = QHBoxLayout()
        buttons_layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )  # Spacer to align buttons to the right

        login_button = QPushButton("Log in", self)
        login_button.setFixedSize(80, 30)
        login_button.clicked.connect(self.check_credentials)

        close_button = QPushButton("Close", self)
        close_button.setFixedSize(80, 30)
        close_button.clicked.connect(self.close)

        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(close_button)
        main_layout.addLayout(buttons_layout)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_encrypted_data(self):
        """Loads and decrypts the user data from encrypted JSON file."""
        key = os.getenv("DART_KEY")
        if not key:
            QMessageBox.critical(self, "Error", "Encryption key not found!")
            return None

        cipher = Fernet(key.encode())
        try:
            with open("encrypted_users.json", "rb") as file:
                encrypted_data = file.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            user_data = json.loads(decrypted_data)
            return user_data
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load user data: {e}")
            return None

    def check_credentials(self):
        """Validates the entered username and password against stored data."""
        user_data = self.load_encrypted_data()
        if not user_data:
            return

        entered_username = self.username_input.text()
        entered_password = self.password_input.text().encode("utf-8")

        for user in user_data["users"]:
            if user["username"] == entered_username:
                if bcrypt.checkpw(entered_password, user["password"].encode("utf-8")):
                    # QMessageBox.information(self, "Login Successful", "Welcome!")
                    self.on_login_success()
                    self.close()
                    return
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
                    return

        QMessageBox.warning(self, "Login Failed", "Username not found.")
