import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Import internal modules
from database.manager import init_db
from ui.views.auth_window import AuthWindow
from ui.views.zoo_app import ZooApp

def main():
    init_db()
    app = QApplication(sys.argv)
    app.setApplicationName("ZooBase")

    # Try to set a nice font
    for family in ["Segoe UI", "SF Pro Display", "Helvetica Neue", "Arial"]:
        font = QFont(family, 10)
        app.setFont(font)
        break

    auth_window = AuthWindow()
    
    def on_login_success():
        auth_window.close()
        global zoo_window
        zoo_window = ZooApp()
        zoo_window.show()

    auth_window.login_successful.connect(on_login_success)
    auth_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
