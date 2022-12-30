# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox, QListWidgetItem, QPushButton

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import BotApiException
from desktop_constructor_app.constructor_app.widgets.ui_sign_up_form import Ui_SignUpForm


class EmptyServerAddressException(Exception):
    pass


class SignUpForm(QWidget):
    """
    Окно регистрации.
    """
    sign_up_success_signal = Signal()
    sign_up_close_signal = Signal()
    sign_up_server_address_error_signal = Signal()

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApiByRequests):
        super().__init__(parent)
        self.server_addr = ''
        self._bot_api = bot_api
        self._ui = Ui_SignUpForm()
        self._ui.setupUi(self)
        self._ui.sign_up_user_button.clicked.connect(self._on_sing_up_form_sign_up)

    def _on_sing_up_form_sign_up(self, checked):
        username: QLineEdit = self._ui.username_line_edit
        email: QLineEdit = self._ui.email_line_edit
        password: QLineEdit = self._ui.password_line_edit
        confirm_password: QLineEdit = self._ui.confirm_password_line_edit
        print(f'Server_addr is: {self.server_addr}')
        if password.text() == confirm_password.text():
            try:
                if not self.server_addr:
                    raise EmptyServerAddressException('It is necessary to fill in the server address '
                                                      'fields on the previous screen. '
                                                      'For example: https://ramasuchka.kz/')
                self._bot_api.set_suite(self.server_addr)
                self._bot_api.sign_up(
                    username=username.text(),
                    email=email.text(),
                    password=password.text()
                )
                QMessageBox.information(self, 'Success', f'User {username.text()} created successfully')
                self.sign_up_success_signal.emit()
            except BotApiException as bot_api_exception:
                QMessageBox.critical(self, 'Error', str(bot_api_exception))
            except EmptyServerAddressException as exception:
                QMessageBox.warning(self, 'Server address error', str(exception))
                self.sign_up_server_address_error_signal.emit()
        else:
            QMessageBox.warning(self, 'Password error', 'Passwords don\'t match')

    def closeEvent(self, event: QCloseEvent) -> None:
        self.sign_up_close_signal.emit()
        event.accept()
