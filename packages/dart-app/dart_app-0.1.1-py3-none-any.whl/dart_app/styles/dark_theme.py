dark_theme = """
    /* General background color for the entire application */
    QWidget {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }

    /* Main window style */
    QMainWindow {
        background-color: #2D2D2D;
    }

    /* Labels */
    QLabel {
        color: #E0E0E0;
        font-size: 14px;
    }

    /* QLineEdit (darker background for input fields with thinner borders) */
    QLineEdit {
        background-color: #1E1E1E;  /* Darker shade for input fields */
        border: 1px solid #4A4A4A;  /* Thinner border */
        padding: 6px;
        color: #FFFFFF;
    }

    /* QPushButton (square buttons with thinner borders) */
    QPushButton {
        background-color: #3C3C3C;  /* Dark gray for buttons */
        color: #FFFFFF;
        padding: 6px;
        font-weight: bold;
        border: 1px solid #4A4A4A;  /* Thinner border */
    }
    QPushButton:hover {
        background-color: #4A4A4A;  /* Slightly lighter for hover effect */
    }
    QPushButton:pressed {
        background-color: #2D2D2D;  /* Slightly darker for pressed effect */
    }

    /* MessageBox */
    QMessageBox {
        background-color: #3C3C3C;
        color: #FFFFFF;
    }

    /* Scroll bars */
    QScrollBar:vertical {
        background-color: #2D2D2D;
        width: 12px;
        margin: 15px 3px 15px 3px;
        border: 1px solid #3C3C3C;
    }
    QScrollBar::handle:vertical {
        background-color: #4A4A4A;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    /* Tooltips */
    QToolTip {
        color: #FFFFFF;
        background-color: #4A4A4A;
        border: none;
    }
"""
