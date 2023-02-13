# This Python file uses the following encoding: utf-8
import typing
from enum import Enum

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox, QListWidgetItem

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription
from common.localisation import tran
from utils.name_utils import gen_next_name
from constructor_app.settings.login_settings_manager import LoginSettingsManager
from constructor_app.settings.get_application_data_dir import get_application_data_dir
from constructor_app.widgets.ui_login_form import Ui_LoginForm
from constructor_app.settings.login_settings import LoginSettings


class LoginStateEnum(Enum):
    """
    Текущее состояние окна логина
    """

    # состояние подключения к серверу
    LOGIN = 'login'

    # состояние работы со списком ботов
    BOTS = 'bots'


class LoginForm(QWidget):
    """
    Окно с логином и выбором бота
    """

    _LIST_DATA_ROLE = QtCore.Qt.UserRole + 1

    _LOGO_HEIGHT = 150

    open_bot_signal = Signal(BotDescription)
    sign_up_signal = Signal(str)

    _KEY = b'OCbAwQH4JA9ID-5gJB4nvk4UbNwpHx4wNT5O5VNKcGI='

    def __init__(self, parent: typing.Optional[QWidget], bot_api: IBotApi):
        super().__init__(parent)
        self._bot_api = bot_api
        self._ui = Ui_LoginForm()
        self._ui.setupUi(self)
        logo_pixmap = QPixmap(':/icons/images/cuttle_systems_logo.png')
        if logo_pixmap.height() > 0:
            logo_aspect_ratio = float(logo_pixmap.width()) / logo_pixmap.height()
            self._ui.cuttle_systems_logo_label.setFixedSize(
                int(logo_aspect_ratio * self._LOGO_HEIGHT),
                self._LOGO_HEIGHT)
            self._ui.cuttle_systems_logo_label.setPixmap(logo_pixmap)
        else:
            print('Can not load logo')

        settings_path = get_application_data_dir()
        self._application_settings = LoginSettingsManager(settings_path, key=self._KEY)
        settings = self._application_settings.read_settings()
        state = Qt.CheckState.Checked if settings.save_password else Qt.CheckState.Unchecked
        self._ui.save_my_password.setCheckState(state)
        self._ui.username_edit.setText(settings.name)
        self._ui.password_edit.setText(settings.password)
        self._ui.server_addr_edit.setText(settings.address)
        self._connect_signals()
        self._dialog_state: LoginStateEnum = LoginStateEnum.LOGIN
        self._activate_controls()

    def _save_settings(self, settings: LoginSettings) -> None:
        assert isinstance(settings, LoginSettings)
        self._application_settings.write_settings(settings)

    def _connect_signals(self):
        self._ui.load_bots.clicked.connect(self._on_load_bots_click)
        self._ui.open_bot_button.clicked.connect(self._on_open_bot_click)
        self._ui.delete_bot_button.clicked.connect(self._on_delete_bot_click)
        self._ui.create_bot_button.clicked.connect(self._on_create_bot_click)
        self._ui.change_user_button.clicked.connect(self._on_change_user_click)
        self._ui.bot_list_widget.currentItemChanged.connect(self._on_current_bot_changed)
        self._ui.update_bot_list_button.clicked.connect(self._on_update_bot_list)
        self._ui.sign_up_button.clicked.connect(self._on_sign_up)

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
        self._ui.update_bot_list_button.setEnabled(False)
        self._ui.sign_up_button.setEnabled(False)
        self._ui.save_my_password.setEnabled(False)
        if self._dialog_state == LoginStateEnum.LOGIN:
            self._ui.server_addr_edit.setEnabled(True)
            self._ui.username_edit.setEnabled(True)
            self._ui.password_edit.setEnabled(True)
            self._ui.save_my_password.setEnabled(True)
            self._ui.load_bots.setEnabled(True)
            self._ui.sign_up_button.setEnabled(True)
        elif self._dialog_state == LoginStateEnum.BOTS:
            self._ui.change_user_button.setEnabled(True)
            self._ui.bot_list_widget.setEnabled(True)
            self._ui.create_bot_button.setEnabled(True)
            is_selected_bot = self._ui.bot_list_widget.currentItem() is not None
            self._ui.open_bot_button.setEnabled(is_selected_bot)
            self._ui.delete_bot_button.setEnabled(is_selected_bot)
            self._ui.update_bot_list_button.setEnabled(True)

    def __load_bots_list(self):
        try:
            bots = self._bot_api.get_bots()
            bot_items = []
            self._ui.bot_list_widget.clear()

            running_bots = self._bot_api.get_running_bots_info()
            running_bot_background_color = self.palette().linkVisited()
            for bot in bots:
                bot_item = QListWidgetItem(bot.bot_name)
                if bot.id in running_bots:
                    bot_item.setBackground(running_bot_background_color)
                    bot_item.setText(f'{bot.bot_name} --> running')
                bot_item.setData(self._LIST_DATA_ROLE, bot)
                bot_items.append(bot_item)
                self._ui.bot_list_widget.addItem(bot_item)
        except BotApiException as error:
            QMessageBox.warning(self, self._tr('Error'), str(error))

    def login_to_server(self):
        server_addr_edit: QLineEdit = self._ui.server_addr_edit
        username_edit: QLineEdit = self._ui.username_edit
        password_edit: QLineEdit = self._ui.password_edit

        try:
            self._bot_api.set_suite(server_addr_edit.text())
            self._bot_api.authentication(username_edit.text(), password_edit.text())
            self._dialog_state = LoginStateEnum.BOTS
            self.__load_bots_list()
            self._activate_controls()
            settings = LoginSettings(
                address=server_addr_edit.text(),
                name=username_edit.text(),
                password=None,
                save_password=True
            )
            if self._ui.save_my_password.checkState() == Qt.CheckState.Checked:
                settings.password = password_edit.text()
            else:
                settings.save_password = False
            self._save_settings(settings)
        except BotApiException as bot_api_exception:
            QMessageBox.critical(self, self._tr('Error'), str(bot_api_exception))

    def _on_load_bots_click(self, _checked: bool):
        self.login_to_server()

    def _on_open_bot_click(self, _checked: bool):
        selected_item: typing.Optional[QListWidgetItem] = self._ui.bot_list_widget.currentItem()
        if selected_item is not None:
            selected_bot = selected_item.data(self._LIST_DATA_ROLE)
            self.open_bot_signal.emit(selected_bot)
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
        # сначала обновим список ботов, чтобы получить актуальный набор названий,
        # потому что от него будет зависеть следующее имя бота
        self.__load_bots_list()
        try:
            bot = self._bot_api.create_bot(
                bot_name=self.__get_unique_bot_name(self._tr('New Cuttle Systems bot')),
                bot_token='',
                bot_description='')
        except BotApiException as error:
            QMessageBox.warning(self, self._tr('Error'), self._tr('Bot creation error: {0}').format(error))
        # теперь обновим список ботов, чтобы увидеть нового созданного бота в списке
        self.__load_bots_list()

    def _on_change_user_click(self, _checked: bool):
        self._ui.bot_list_widget.clear()
        self._dialog_state = LoginStateEnum.LOGIN
        self._activate_controls()

    def _on_current_bot_changed(self, _item):
        print('_on_current_bot_changed')
        self._activate_controls()

    def _on_update_bot_list(self, _checked: bool):
        self.__load_bots_list()

    def __get_all_bots(self) -> typing.List[BotDescription]:
        all_bots = []
        for index in range(self._ui.bot_list_widget.count()):
            item: QListWidgetItem = self._ui.bot_list_widget.item(index)
            bot: BotDescription = item.data(self._LIST_DATA_ROLE)
            assert isinstance(bot, BotDescription)
            all_bots.append(bot)
        return all_bots

    def __get_unique_bot_name(self, base_name: str) -> str:
        used_names = [bot.bot_name for bot in self.__get_all_bots()]
        return gen_next_name(base_name, used_names)

    def _on_sign_up(self, _checked: bool):
        if not self._ui.server_addr_edit.text():
            QMessageBox.warning(
                self,
                self._tr('Server address error'),
                self._tr(
                    'Please fill in the server address field. '
                    'For example: https://ramasuchka.kz/')
            )
        else:
            self.sign_up_signal.emit(self._ui.server_addr_edit.text())

    def _tr(self, mes: str) -> str:
        return tran('LoginForm.manual', mes)
