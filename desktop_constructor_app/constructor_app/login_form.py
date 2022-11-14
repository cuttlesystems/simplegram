# This Python file uses the following encoding: utf-8
import os
import typing
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QListView, QListWidget, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from b_logic.bot_api import BotApi, BotApiException


class LoginForm(QWidget):
    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApi):
        super().__init__(parent)
        self._bot_api = bot_api
        self._load_ui()
        self._connect_signals()

    def _load_ui(self):
        loader = QUiLoader()
        path = Path(__file__).resolve().parent / "login_form.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self._ui = loader.load(ui_file, self)
        ui_file.close()

    def _connect_signals(self):
        self._ui.load_bots.clicked.connect(self._on_button_click)

    def _on_button_click(self):
        bot_list_widget: QListWidget = self._ui.bot_list_widget
        bot_list_widget.clear()
        server_addr_edit: QLineEdit = self._ui.server_addr_edit
        username_edit: QLineEdit = self._ui.username_edit
        password_edit: QLineEdit = self._ui.password_edit
        try:
            self._bot_api.set_suite(server_addr_edit.text())
            self._bot_api.authentication(username_edit.text(), password_edit.text())
            bots = self._bot_api.get_bots()
            bots_names = [bot.bot_name for bot in bots]
            bot_list_widget.addItems(bots_names)
        except BotApiException as error:
            QMessageBox.warning(self, 'Ошибка', str(error))

