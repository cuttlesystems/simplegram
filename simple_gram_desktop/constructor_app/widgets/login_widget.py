import typing

from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox
from PySide6.QtCore import QObject, Slot, Signal, QThread

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import BotApiException
from common.localisation import tran
from constructor_app.settings.get_application_data_dir import get_application_data_dir
from constructor_app.settings.login_settings import LoginSettings
from constructor_app.settings.login_settings_manager import LoginSettingsManager

from constructor_app.widgets.ui_login_widget import Ui_LoginWidget

class LoginWidget(QWidget):
    # сигнал, что пользователь авторизовался
    log_in = Signal()
    registrated_state_signal = Signal(bool)
    _KEY = b'OCbAwQH4JA9ID-5gJB4nvk4UbNwpHx4wNT5O5VNKcGI='

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_LoginWidget()
        self._ui.setupUi(self)
        self.bot_api = BotApiByRequests()

        settings_path = get_application_data_dir()
        self._application_settings = LoginSettingsManager(settings_path, key=self._KEY)
        settings = self._application_settings.read_settings()
        self._ui.username_edit.setText(settings.name)
        self._ui.password_widget.setText(settings.password)
        self._ui.server_addr_edit.setText(settings.address)

        # подключаю кнопку ентерПользователя с переходом на мейнОкно
        self._ui.enter_button.clicked.connect(self._clicked_login)
        # toDO: Добавить функцию инициализации QSS

    def _clicked_login(self):
        server_addr_edit: QLineEdit = self._ui.server_addr_edit
        username_edit: QLineEdit = self._ui.username_edit
        password_edit: QLineEdit = self._ui.password_widget
        try:
            self.bot_api.set_suite(server_addr_edit.text())
            self.bot_api.authentication(username_edit.text(), password_edit.text())
            settings = LoginSettings(
                address=server_addr_edit.text(),
                name=username_edit.text(),
                password=None,
                save_password=True
            )
            settings.password = password_edit.text()
            self._application_settings.write_settings(settings)
        except BotApiException as bot_api_exception:
            QMessageBox.critical(self, self._tr('Error'), str(bot_api_exception))
        self.log_in.emit()



    def _switch_login(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой
        #  первострочный инициализатор qss и доработать режим входа/регистрации
        #if (self._ui.switchActivatedBot.isChecked()):
        #    self._ui.markerActivisionBot.setStyleSheet("QLabel{border-radius:8px; border:none; color:white;"
        #                                                   "background-color:#4DAAFF;}")
        #    self._ui.markerActivisionBot.setText(u"Бот запущен")
        #    self.ActivatedBotSignal.emit(True)
        #else:
        #    self._ui.markerActivisionBot.setStyleSheet("QLabel{border-radius:8px; border:none; color:white;"
        #                                                   "background-color:#FF5F8F;}")
        #    self._ui.markerActivisionBot.setText(u"Бот не активен")
        self.registrated_state_signal.emit(False)

    def _tr(self, text: str) -> str:
        return tran('LoginWidget.manual', text)
