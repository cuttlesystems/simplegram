# This Python file uses the following encoding: utf-8
import typing
from enum import Enum

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QMessageBox, QListWidgetItem

from b_logic.bot_api import BotApi, BotApiException
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.bot_editor_form import BotEditorForm
from desktop_constructor_app.constructor_app.ui_login_form import Ui_LoginForm


class LoginStateEnum(Enum):
    LOGIN = 'login'
    BOTS = 'bots'


class LoginForm(QWidget):
    _LIST_DATA_ROLE = 175438

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApi):
        super().__init__(parent)
        self._bot_api = bot_api
        self._ui = Ui_LoginForm()
        self._ui.setupUi(self)
        self._connect_signals()
        self._bot_editor_form = BotEditorForm(None)
        self._dialog_state: LoginStateEnum = LoginStateEnum.LOGIN
        self._activate_controls()

    def _connect_signals(self):
        self._ui.load_bots.clicked.connect(self._on_load_bots_click)
        self._ui.open_bot_button.clicked.connect(self._on_open_bot_click)
        self._ui.delete_bot_button.clicked.connect(self._on_delete_bot_click)
        self._ui.create_bot_button.clicked.connect(self._on_create_bot_click)

    def _activate_controls(self):
        self._ui.server_addr_edit.setEnabled(False)
        self._ui.username_edit.setEnabled(False)
        self._ui.password_edit.setEnabled(False)
        self._ui.load_bots.setEnabled(False)
        self._ui.change_user_button.setEnabled(False)
        self._ui.bot_list_widget.setEnabled(False)
        self._ui.open_bot_button.setEnabled(False)
        self._ui.create_bot_button.setEnabled(False)
        self._ui.delete_bot_button.setEnabled(False)
        if self._dialog_state == LoginStateEnum.LOGIN:
            self._ui.server_addr_edit.setEnabled(True)
            self._ui.username_edit.setEnabled(True)
            self._ui.password_edit.setEnabled(True)
            self._ui.load_bots.setEnabled(True)
        elif self._dialog_state == LoginStateEnum.BOTS:
            self._ui.change_user_button.setEnabled(True)
            self._ui.bot_list_widget.setEnabled(True)
            self._ui.create_bot_button.setEnabled(True)
            is_selected_bot = self._ui.bot_list_widget.currentItem() is None
            self._ui.open_bot_button.setEnabled(is_selected_bot)
            self._ui.delete_bot_button.setEnabled(is_selected_bot)

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

        try:
            self._bot_api.set_suite(server_addr_edit.text())
            self._bot_api.authentication(username_edit.text(), password_edit.text())
            self._dialog_state = LoginStateEnum.BOTS
            self._activate_controls()
        except BotApiException as bot_api_exception:
            QMessageBox.critical(self, 'Ошибка', str(bot_api_exception))

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

    def _on_create_bot_click(self, _checked: bool):
        self.__load_bots_list()
        bot = self._bot_api.create_bot(
            self.__get_unique_bot_name('Новый Cuttle Systems бот'), '', '')
        self.__load_bots_list()

    def __get_all_bots(self) -> typing.List[BotDescription]:
        all_bots = []
        for index in range(self._ui.bot_list_widget.count()):
            item: QListWidgetItem = self._ui.bot_list_widget.item(index)
            bot: BotDescription = item.data(self._LIST_DATA_ROLE)
            assert isinstance(bot, BotDescription)
            all_bots.append(bot)
        return all_bots

    def __get_unique_bot_name(self, base_name: str):
        used_names = [bot.bot_name for bot in self.__get_all_bots()]
        test_name = base_name
        n = 2
        while test_name in used_names:
            test_name = f'{base_name} {n}'
            n += 1
        return test_name
