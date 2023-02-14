import typing

from PySide6 import QtGui
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QPalette, QResizeEvent
from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox
from PySide6.QtCore import QObject, Slot, Signal, QThread, QSize, QPoint, QRect, Qt

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import BotApiException
from common.localisation import tran
from constructor_app.settings.get_application_data_dir import get_application_data_dir
from constructor_app.settings.login_settings import LoginSettings
from constructor_app.settings.login_settings_manager import LoginSettingsManager

from constructor_app.widgets.ui_login_widget import Ui_LoginWidget
from network.bot_api_by_request_extended import BotApiByRequestsProxy


class LoginWidget(QWidget):
    # сигнал, что пользователь авторизовался
    log_in = Signal(BotApiByRequests)
    registrated_state_signal = Signal(bool)
    _KEY = b'OCbAwQH4JA9ID-5gJB4nvk4UbNwpHx4wNT5O5VNKcGI='

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_LoginWidget()
        self._ui.setupUi(self)
        self.bot_api = BotApiByRequestsProxy()

        # заполнение полей данными при логине
        settings_path = get_application_data_dir()
        self._application_settings = LoginSettingsManager(settings_path, key=self._KEY)
        self._set_login_mode()

        # подключаю кнопку ентерПользователя с переходом на мейнОкно
        self._ui.login_button.clicked.connect(self._clicked_login_button)
        # toDO: Добавить функцию инициализации QSS
        self.installEventFilter(self)

        # подключаю кнопку регистрации
        self._ui.sign_up_user_button.clicked.connect(self._clicked_sign_up_button)

        # подключаю переключатель логин/регистрация
        self._ui.registrate_radiobutton.toggled.connect(self._toggled_registration)

        #size = self.size()
        ##QPixmap(":/icons/widgets/times_icon/background_texture.png").scaled(size, Qt.AspectRatioMode.IgnoreAspectRatio)
        #background_img = QBrush(QColor(0, 0, 0))
        #palette = QPalette()
        #palette.setBrush(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Window, background_img)
        #self.setPalette(palette)

        # self.setStyleSheet("#LoginWidget{ border-image: url(:/icons/widgets/times_icon/background_texture.png);}")


    def _clicked_login_button(self):
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

    def _clicked_sign_up_button(self):
        server_addr: QLineEdit = self._ui.server_addr_edit
        username: QLineEdit = self._ui.username_edit
        email: QLineEdit = self._ui.email_edit
        password: QLineEdit = self._ui.password_edit
        confirm_password: QLineEdit = self._ui.confirm_password_edit
        required_fields: typing.List[QLineEdit] = [server_addr, email, username, password, confirm_password]
        unfilled_field: typing.Optional[QLineEdit] = None
        for field in required_fields:
            if not field.text():
                unfilled_field = field
                break
        if unfilled_field is not None:
            QMessageBox.warning(self,
                                self._tr('Empty field error'),
                                self._tr('{field}. This field should not be empty.').format(field=unfilled_field.placeholderText())
                                )
        elif password.text() == confirm_password.text():
            try:
                self.bot_api.set_suite(server_addr.text())
                self.bot_api.sign_up(
                    username=username.text(),
                    email=email.text(),
                    password=password.text()
                )
                QMessageBox.information(self,
                                        self._tr('Success'),
                                        self._tr('User {username} created successfully.').format(username=username.text())
                                        )
                # если пользователь успешно создан переключиться в режим логин
                self._ui.login_radiobutton.setChecked(True)
            except BotApiException as bot_api_exception:
                QMessageBox.critical(self, self._tr('Error'), str(bot_api_exception))
        else:
            QMessageBox.warning(self, self._tr('Password error'), self._tr('Passwords did not match.'))

    def _switch_login(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой
        #  первострочный инициализатор qss и доработать режим входа/регистрации
        self.registrated_state_signal.emit(False)

    def _toggled_registration(self):
        if self._ui.registrate_radiobutton.isChecked():
            self._set_registration_mode()
        elif self._ui.login_radiobutton.isChecked():
            self._set_login_mode()

    def _set_registration_mode(self):
        # скрыть ненужные и показать нужные поля
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

    def paintEvent(self, event: QPaintEvent) -> None:
        # toDo: If this will be used in the future, then put the colors in the parameters
        qp = QPainter(self)
        background = QLinearGradient()
        background.setStart(QPoint(self.width()/2, 0))
        background.setFinalStop(QPoint(self.width()/2, self.height()))
        background.setColorAt(0, QColor(57, 178, 146))
        background.setColorAt(0.5, QColor(68, 159, 167))
        background.setColorAt(1, QColor(82, 136, 193))
        qp.setBrush(QBrush(background))
        qp.drawRect(QRect(0, 0, self.width(), self.height()))
        pixmap = QPixmap(":icons/widgets/times_icon/background_texture.png")
        qp.drawPixmap(0, 0, QPixmap(":icons/widgets/times_icon/background_texture.png").scaled(self.size()))
        qp.end()

    def _tr(self, text: str) -> str:
        return tran('LoginWidget.manual', text)
