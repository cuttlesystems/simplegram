# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QMessageBox, QListWidgetItem

from b_logic.bot_api import BotApi, BotApiException
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.bot_editor_form import BotEditorForm
from desktop_constructor_app.constructor_app.ui_login_form import Ui_LoginForm


class LoginForm(QWidget):
    _LIST_DATA_ROLE = 175438

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApi):
        super().__init__(parent)
        self._bot_api = bot_api
        self._ui = Ui_LoginForm()
        self._ui.setupUi(self)
        self._connect_signals()
        self._bot_editor_form = BotEditorForm(None)

    def _connect_signals(self):
        self._ui.load_bots.clicked.connect(self._on_load_bots_click)
        self._ui.open_bot_button.clicked.connect(self._on_open_bot_click)
        self._ui.delete_bot_button.clicked.connect(self._on_delete_bot_click)

    def __load_bots_list(self):
        try:
            bots = self._bot_api.get_bots()
            bot_items = []
            self._ui.bot_list_widget.clear()
            for bot in bots:
                bot_item = QListWidgetItem(bot.bot_name)
                bot_item.setData(self._LIST_DATA_ROLE, bot)
                bot_items.append(bot_item)
                self._ui.bot_list_widget.addItem(bot_item)
        except BotApiException as error:
            QMessageBox.warning(self, 'Ошибка', str(error))

    def _on_load_bots_click(self, _checked: bool):

        server_addr_edit: QLineEdit = self._ui.server_addr_edit
        username_edit: QLineEdit = self._ui.username_edit
        password_edit: QLineEdit = self._ui.password_edit

        self._bot_api.set_suite(server_addr_edit.text())
        self._bot_api.authentication(username_edit.text(), password_edit.text())

        self.__load_bots_list()

    def _on_open_bot_click(self, _checked: bool):
        selected_item: typing.Optional[QListWidgetItem] = self._ui.bot_list_widget.currentItem()
        if selected_item is not None:
            selected_bot = selected_item.data(self._LIST_DATA_ROLE)
            self._bot_editor_form.set_bot(selected_bot)
            self._bot_editor_form.show()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не выбран бот')

    def _on_delete_bot_click(self, _checked: bool):
        selected_item: typing.Optional[QListWidgetItem] = self._ui.bot_list_widget.currentItem()
        if selected_item is not None:
            selected_bot: BotDescription = selected_item.data(self._LIST_DATA_ROLE)
            self._bot_api.delete_bot(selected_bot.id)
            self.__load_bots_list()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не выбран бот')