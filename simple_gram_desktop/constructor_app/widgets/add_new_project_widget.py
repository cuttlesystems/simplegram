import typing

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette,QColor,QBrush
from PySide6.QtCore import QObject, Slot, Signal, QThread


from constructor_app.widgets.ui_add_new_project_widget import Ui_AddNewProjectWidget

class AddNewProjectWidget(QWidget):
    close_window = Signal()
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_AddNewProjectWidget()
        self._ui.setupUi(self)

        # подключаю кнопку закрыть добавление проекта с переходом на мейнОкно
        self._ui.close_button.clicked.connect(self._clicked_сlose)

    def _init_stylesheet(self,night)->None:
        if (night):
            self.setPalette(QBrush(QColor(27,27,27,155)),QPalette.window())
        else:
            self.setPalette(QBrush(QColor(27,27,27,155)), QPalette.window())

    def _clicked_сlose(self):
        self.close_window.emit()