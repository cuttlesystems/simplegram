import typing

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette,QColor,QBrush
from PySide6.QtCore import QObject, Slot, Signal, QThread

from common.localisation import tran

from constructor_app.widgets.ui_tool_stack_widget import Ui_ToolStackWidget

class ToolStackWidget(QWidget):
    add_new_message_signal = Signal()
    action_add_variant_signal = Signal()
    delete_message_signal = Signal()
    generate_bot_signal = Signal()
    start_bot_signal = Signal()
    stop_bot_signal = Signal()
    mark_as_start_signal = Signal()
    mark_as_error_signal = Signal()
    delete_variant_signal = Signal()
    read_bot_logs_signal = Signal()

    def __init__(self, parent: typing.Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)
        self._ui = Ui_ToolStackWidget()
        self._ui.setupUi(self)

        # подключаю кнопку закрыть добавление проекта и отмена добавления проекта с переходом на мейнОкно
        self._ui.add_message_button.clicked.connect(self._on_add_new_message)
        self._ui.add_variant_button.clicked.connect(self._on_action_add_variant)
        self._ui.delete_message_button.clicked.connect(self._on_delete_message)
        self._ui.generate_bot_button.clicked.connect(self._on_generate_bot)
        self._ui.start_bot_button.clicked.connect(self._on_start_bot)
        self._ui.stop_bot_button.clicked.connect(self._on_stop_bot)
        self._ui.mark_start_message_button.clicked.connect(self._on_mark_as_start)
        self._ui.mark_error_message_button.clicked.connect(self._on_mark_as_error)
        self._ui.delete_variant_button.clicked.connect(self._on_delete_variant)

        #self._ui.action_manual_save_button.triggered.connect(self._on_apply_button)
        #self._ui.action_read_logs_button.triggered.connect(self._on_read_bot_logs)

    def _on_add_new_message(self) -> None:
        self.add_new_message_signal.emit()

    def _on_action_add_variant(self) -> None:
        self.action_add_variant_signal.emit()

    def _on_delete_message(self) -> None:
        self.delete_message_signal.emit()

    def _on_generate_bot(self) -> None:
        self.generate_bot_signal.emit()

    def _on_start_bot(self) -> None:
        self.start_bot_signal.emit()

    def _on_stop_bot(self) -> None:
        self.stop_bot_signal.emit()

    def _on_mark_as_start(self) -> None:
        self.mark_as_start_signal.emit()

    def _on_mark_as_error(self) -> None:
        self.mark_as_error_signal.emit()

    def _on_delete_variant(self) -> None:
        self.delete_variant_signal.emit()

    def _on_read_bot_logs(self) -> None:
        self.read_bot_logs_signal.emit()

    def _init_stylesheet(self, night: bool)->None:
        # toDO: поменять даркмод режим на изменение qssа и все qss вынести в отдельный файлпроекта или
        #  для каждого окна сделать свой первострочный инициализатор qss
        if night:
            self.setPalette(QBrush(QColor(27, 27, 27, 155)), QPalette.window())
        else:
            self.setPalette(QBrush(QColor(27, 27, 27, 155)), QPalette.window())


    def _tr(self, text: str) -> str:
        return tran('AddNewProjectWidget.manual', text)