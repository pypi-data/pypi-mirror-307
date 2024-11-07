from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QFrame,
    QToolBar,
)


class MainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DART - Main Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("resources/dart_icon.svg"))

        # Set up the main layout
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create the sidebar
        self.create_sidebar()

        # Create the top navigation bar
        self.create_top_nav()

        # Create the central display area
        self.central_display = QStackedWidget()
        main_layout.addWidget(self.central_display)

        # Add placeholders for each section
        self.create_section_placeholders()

        # Set initial view to Home
        self.central_display.setCurrentWidget(self.home_widget)

    def create_top_nav(self):
        # Top Navigation Bar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Add navigation actions
        home_action = QAction("Home", self)
        home_action.triggered.connect(self.show_home)
        toolbar.addAction(home_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)

        scripts_action = QAction("Scripts", self)
        scripts_action.triggered.connect(self.show_scripts)
        toolbar.addAction(scripts_action)

        destinations_action = QAction("Destinations", self)
        destinations_action.triggered.connect(self.show_destinations)
        toolbar.addAction(destinations_action)

    def create_sidebar(self):
        # Sidebar Frame
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar_frame.setLayout(sidebar_layout)

        # DICOM Sources section
        dicom_sources_label = QLabel("DICOM Sources")
        dicom_sources_label.setStyleSheet("font-weight: bold; color: #FFFFFF;")
        sidebar_layout.addWidget(dicom_sources_label)

        # User Management section (admin only)
        user_management_label = QLabel("User Management")
        user_management_label.setStyleSheet("font-weight: bold; color: #FFFFFF;")
        sidebar_layout.addWidget(user_management_label)

        self.centralWidget().layout().addWidget(sidebar_frame)

    def create_section_placeholders(self):
        # Placeholder widgets for each section
        self.home_widget = QLabel("Home - Quick Overview")
        self.settings_widget = QLabel("Settings - Configuration Options")
        self.scripts_widget = QLabel("Scripts - Manage DICOM Processing Scripts")
        self.destinations_widget = QLabel("Destinations - Manage DICOM Destinations")

        # Add widgets to the central display stack
        self.central_display.addWidget(self.home_widget)
        self.central_display.addWidget(self.settings_widget)
        self.central_display.addWidget(self.scripts_widget)
        self.central_display.addWidget(self.destinations_widget)

    # Methods to switch views in central display
    def show_home(self):
        self.central_display.setCurrentWidget(self.home_widget)

    def show_settings(self):
        self.central_display.setCurrentWidget(self.settings_widget)

    def show_scripts(self):
        self.central_display.setCurrentWidget(self.scripts_widget)

    def show_destinations(self):
        self.central_display.setCurrentWidget(self.destinations_widget)

    def logout(self):
        self.close()
