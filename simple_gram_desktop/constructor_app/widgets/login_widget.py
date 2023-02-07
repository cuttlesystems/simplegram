import typing

from PySide6.QtGui import Qt
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
    log_in = Signal(BotApiByRequests)
    registrated_state_signal = Signal(bool)
    _KEY = b'OCbAwQH4JA9ID-5gJB4nvk4UbNwpHx4wNT5O5VNKcGI='

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_LoginWidget()
        self._ui.setupUi(self)
        self.bot_api = BotApiByRequests()

        # заполнение полей данными при логине
        settings_path = get_application_data_dir()
        self._application_settings = LoginSettingsManager(settings_path, key=self._KEY)
        self._set_login_mode()

        # подключаю кнопку ентерПользователя с переходом на мейнОкно
        self._ui.login_button.clicked.connect(self._clicked_login)
        # toDO: Добавить функцию инициализации QSS
        # подключаю
        self._ui.registrate_radiobutton.toggled.connect(self._toggled_registration)

    def _clicked_login(self):
        server_addr_edit: QLineEdit = self._ui.server_addr_edit
        username_edit: QLineEdit = self._ui.username_edit
        password_edit: QLineEdit = self._ui.password_edit
        try:
            self.bot_api.set_suite(server_addr_edit.text())
            self.bot_api.authentication(username_edit.text(), password_edit.text())
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
            self._application_settings.write_settings(settings)

            self.log_in.emit(self.bot_api)
        except BotApiException as bot_api_exception:
            QMessageBox.critical(self, self._tr('Error'), str(bot_api_exception))

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

    def _toggled_registration(self):
        if self._ui.registrate_radiobutton.isChecked():
            self._set_registration_mode()

        elif self._ui.login_radiobutton.isChecked():
            self._set_login_mode()

    def _set_registration_mode(self):
        # скрыть ненужные и показать нужные поля
        self._ui.server_addr_edit.hide()
        self._ui.email_edit.show()
        self._ui.confirm_password_edit.show()
        self._ui.save_my_password.hide()
        self._ui.login_button.hide()
        self._ui.sign_up_user_button.show()

        # отчистить поля от информации
        self._ui.email_edit.clear()
        self._ui.username_edit.clear()
        self._ui.password_edit.clear()
        self._ui.confirm_password_edit.clear()

    def _set_login_mode(self):
        # скрыть ненужные и показать нужные поля
        self._ui.server_addr_edit.show()
        self._ui.email_edit.hide()
        self._ui.confirm_password_edit.hide()
        self._ui.save_my_password.show()
        self._ui.login_button.show()
        self._ui.sign_up_user_button.hide()

        # заполнить поля сохраненными данными
        settings = self._application_settings.read_settings()
        state = Qt.CheckState.Checked if settings.save_password else Qt.CheckState.Unchecked
        self._ui.save_my_password.setCheckState(state)
        self._ui.username_edit.setText(settings.name)
        self._ui.password_edit.setText(settings.password)
        self._ui.server_addr_edit.setText(settings.address)

    def _tr(self, text: str) -> str:
        return tran('LoginWidget.manual', text)
