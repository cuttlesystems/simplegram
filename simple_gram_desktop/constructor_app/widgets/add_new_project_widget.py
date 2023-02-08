import typing

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPalette,QColor,QBrush
from PySide6.QtCore import QObject, Slot, Signal, QThread
from PySide6 import QtCore

from common.localisation import tran
from b_logic.bot_api.i_bot_api import IBotApi, BotApiException, CreatingBotException

from constructor_app.widgets.ui_add_new_project_widget import Ui_AddNewProjectWidget

class AddNewProjectWidget(QWidget):
    close_window = Signal()
    _bot_api: IBotApi
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_AddNewProjectWidget()
        self._ui.setupUi(self)

        # подключаю кнопку закрыть добавление проекта и отмена добавления проекта с переходом на мейнОкно
        self._ui.close_button.clicked.connect(self._clicked_сlose)
        self._ui.cancel_button.clicked.connect(self._clicked_сlose)
        self._ui.accept_button.clicked.connect(self._add_new_bot)

        # toDO: Добавить функцию инициализации QSS
        self._ui.background_father_widget.installEventFilter(self)
        self.setMouseTracking(True)

    def _init_stylesheet(self, night) -> None:
        # toDO: поменять даркмод режим на изменение qssа и все qss вынести в отдельный файлпроекта или
        #  для каждого окна сделать свой первострочный инициализатор qss
        if night:
            self.setPalette(QBrush(QColor(27, 27, 27, 155)), QPalette.window())
        else:
            self.setPalette(QBrush(QColor(27, 27, 27, 155)), QPalette.window())

    def _clicked_сlose(self):
        self.close_window.emit()

    def set_bot_api(self, bot_api: IBotApi):
        self._bot_api = bot_api

    def eventFilter(self, obj: QObject, event: QtCore.QEvent) -> bool:
        if obj == self._ui.background_father_widget:
            if (event.type() == QtCore.QEvent.Type.HoverLeave):
                self._ui.background_father_widget.setStyleSheet("QGroupBox{"
                                                                "border: none;"
                                                                "border-radius: 16px;"
                                                                "background-color: rgba(255,255,255,180);"
                                                                "}")
                self.setFocus()
            if (event.type() == QtCore.QEvent.Type.HoverEnter):
                self._ui.background_father_widget.setStyleSheet("QGroupBox{"
                                                                "border: none;"
                                                                "border-radius: 16px;"
                                                                "background-color: rgb(255,255,255);"
                                                                "}")
            return False
        return QWidget.eventFilter(self, obj, event)

    def _add_new_bot(self):
        try:
            bot = self._bot_api.create_bot(
                bot_name=self._ui.name_bot.text(),
                bot_token=self._ui.token_bot_edit.text(),
                bot_description=self._ui.about_bot_edit.text()
            )
            QMessageBox.information(self, 'created', 'created')
        except Exception as error:
            QMessageBox.warning(self, self._tr('Error'), self._tr('Bot creation error: {0}').format(error))


    def _tr(self, text: str) -> str:
        return tran('AddNewProjectWidget.manual', text)
