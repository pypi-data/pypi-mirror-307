import os
import sys
import logging
from dart_app.config.key_manager import get_or_create_dart_key
from dart_app.config.logging_config import DBLogHandler, FORMATTER
from dart_app.gui.login_window import LoginWindow
from dart_app.gui.setup_window import SetupWindow
from dart_app.gui.main_window import MainDashboard
from dart_app.styles.dark_theme import dark_theme
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


# Configure the main logger
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
db_handler = DBLogHandler()
db_handler.setFormatter(FORMATTER)
logger.addHandler(db_handler)


# Global variable to keep window instances in scope
current_window = None


def main():
    # Initialize the DART_KEY
    get_or_create_dart_key()

    app = QApplication(sys.argv)

    icon_path = "resources/dart_icon.svg"
    app.setWindowIcon(QIcon(icon_path))
    app.setStyleSheet(dark_theme)

    # Callback functions to manage window transitions
    def open_login_window():
        global current_window
        current_window = LoginWindow(open_main_window)
        current_window.show()

    def open_main_window():
        global current_window
        current_window = MainDashboard()
        current_window.showMaximized()

    # Check if user data exists
    if os.path.exists("encrypted_users.json"):
        logger.info("Opening Login Window")
        open_login_window()
    else:
        logger.info("Opening Setup Window")
        current_window = SetupWindow(open_login_window)
        current_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
