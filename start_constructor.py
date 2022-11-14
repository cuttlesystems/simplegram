import sys
from PySide6.QtWidgets import QApplication

from b_logic.bot_api import BotApi
from desktop_constructor_app.constructor_app.login_form import LoginForm


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot_api = BotApi()
    widget = LoginForm(None, bot_api)
    widget.show()
    sys.exit(app.exec())
