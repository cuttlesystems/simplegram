import sys
from PySide6.QtWidgets import QApplication
from desktop_constructor_app.constructor_app.windows_manager import WindowsManager


if __name__ == "__main__":
    app = QApplication(sys.argv)

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())
