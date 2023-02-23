import typing

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette, QColor, QBrush, QPaintEvent, QPainter, QAction
from PySide6.QtCore import QObject, Signal, QRect
from PySide6 import QtGui, QtWidgets
from dataclasses import dataclass

from common.localisation import tran

from constructor_app.widgets.ui_tool_stack_widget import Ui_ToolStackWidget

@dataclass(slots=True, frozen=True)
class ColorScheme:
    # цвет фона сообщения
    background_color = 0x292a2f
    #button_color_hover = QColor(70, 170, 255)
    #button_color_pressed = QColor(70, 170, 255, 100)


class ToolStackWidget(QWidget):
    _BORDER_RADIUS_BACKGROUND = 12

    add_message_signal = Signal()
    add_variant_signal = Signal()
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
        # toDO: Добавить инициализацию toolTipов
        super().__init__(parent)
        self._ui = Ui_ToolStackWidget()
        self._ui.setupUi(self)

        # подключаю кнопки к сигналам для передачи на мейнокно
        self._ui.add_message_button.clicked.connect(self._on_add_new_message)
        self._ui.add_variant_button.clicked.connect(self._on_action_add_variant)
        self._ui.delete_message_button.clicked.connect(self._on_delete_message)
        self._ui.generate_bot_button.clicked.connect(self._on_generate_bot)
        self._ui.switch_bot.stateChanged.connect(self._switch_toggle)
        self._ui.mark_start_message_button.clicked.connect(self._on_mark_as_start)
        self._ui.mark_error_message_button.clicked.connect(self._on_mark_as_error)
        self._ui.delete_variant_button.clicked.connect(self._on_delete_variant)
        self._ui.generate_logs_button.clicked.connect(self._on_read_bot_logs)


    def paintEvent(self, event: QPaintEvent) -> None:
        # toDo: If this will be used in the future, then put the colors in the parameters
        paint_engine = QPainter(self)
        paint_engine.setRenderHint(QPainter.Antialiasing, True)
        background = QBrush(QColor(ColorScheme.background_color))
        paint_engine.setBrush(background)
        paint_engine.drawRoundedRect(
            QRect(0, 0, self.width(), self.height()),
            self._BORDER_RADIUS_BACKGROUND,
            self._BORDER_RADIUS_BACKGROUND)
        paint_engine.end()

    def init_switch_toggle(self, state: bool):
        assert isinstance(state, bool)
        self._ui.switch_bot.blockSignals(True)
        try:
            self._ui.switch_bot.setChecked(state)
        finally:
            self._ui.switch_bot.blockSignals(False)

    def _switch_toggle(self, state: int):
        assert isinstance(state, int)
        if state == 0:
            self.stop_bot_signal.emit()
        else:
            self.start_bot_signal.emit()

    def set_delete_variant_enabled(self, enabled: bool):
        assert isinstance(enabled, bool)
        self._ui.delete_variant_button.setEnabled(enabled)

    def set_delete_message_enabled(self, enabled: bool) -> None:
        assert isinstance(enabled, bool)
        self._ui.delete_message_button.setEnabled(enabled)

    def set_mark_start_enabled(self, enabled: bool) -> None:
        assert isinstance(enabled, bool)
        self._ui.mark_start_message_button.setEnabled(enabled)

    def set_generate_bot_enabled(self, enabled: bool) -> None:
        assert isinstance(enabled, bool)
        self._ui.generate_bot_button.setEnabled(enabled)

    def set_mark_error_enabled(self, enabled: bool) -> None:
        assert isinstance(enabled, bool)
        self._ui.mark_error_message_button.setEnabled(enabled)

    def set_add_variant_enabled(self, enabled: bool) -> None:
        assert isinstance(enabled, bool)
        self._ui.add_variant_button.setEnabled(enabled)

    def _on_add_new_message(self, _toggled: bool) -> None:
        self.add_message_signal.emit()

    def _on_action_add_variant(self, _toggled: bool) -> None:
        self.add_variant_signal.emit()

    def _on_delete_message(self, _toggled: bool) -> None:
        self.delete_message_signal.emit()

    def _on_generate_bot(self, _toggled: bool) -> None:
        self.generate_bot_signal.emit()

    def _on_mark_as_start(self, _toggled: bool) -> None:
        self.mark_as_start_signal.emit()

    def _on_mark_as_error(self, _toggled: bool) -> None:
        self.mark_as_error_signal.emit()

    def _on_delete_variant(self, _toggled: bool) -> None:
        self.delete_variant_signal.emit()

    def _on_read_bot_logs(self, _toggled: bool) -> None:
        self.read_bot_logs_signal.emit()

    def _init_stylesheet(self, night: bool) -> None:
        # toDO: поменять даркмод режим на изменение qssа и все qss вынести в отдельный файлпроекта или
        #  для каждого окна сделать свой первострочный инициализатор qss
        if night:
            self.setPalette(QBrush(QColor(27, 27, 27, 155)), QPalette.window())

    def _tr(self, text: str) -> str:
        return tran('AddNewProjectWidget.manual', text)