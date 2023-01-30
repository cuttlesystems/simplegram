import typing

from PySide6.QtWidgets import QWidget

from constructor_app.widgets.ui_login_widget import Ui_LoginWidget

class LoginWidget(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_LoginWidget()
        self._ui.setupUi(self)

        # подключаю кнопку ентерПользователя с переходом на мейнОкно
        #self.connect(self._ui.goButton)