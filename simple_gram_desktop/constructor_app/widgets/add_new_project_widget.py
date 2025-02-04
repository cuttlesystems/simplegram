import typing, traceback
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QObject, Signal
from PySide6 import QtCore

from common.localisation import tran
from b_logic.bot_api.i_bot_api import IBotApi
from utils.name_utils import gen_next_name

from constructor_app.widgets.ui_add_new_project_widget import Ui_AddNewProjectWidget
from network.bot_api_by_request_extended import BotApiMessageException, BotDescription
from constructor_app.widgets.bot_extended import BotExtended


class StatedStylesheetEnum(Enum):
    HOVER = 1
    MISS = 2
    FOCUS = 3
    NORMAL = 4


@dataclass(slots=True, frozen=True)
class BlockColorScheme:
    color_group_hover = "rgb(255,255,255)"
    color_group_miss = "rgba(255,255,255,180)"

    color_line_hover = "rgba(82,136,193,180)"
    color_line_focus = "rgb(82,136,193)"
    color_line_miss = "rgba(55,55,55,128)"
    color_line_normal = "rgb(204,204,204)"


class AddNewProjectWidget(QWidget):
    close_window = Signal()
    new_bot_added = Signal()

    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_AddNewProjectWidget()
        self._ui.setupUi(self)

        self._init_stylesheet(False)
        self.init_placeholder_text_line()

        # подключаю кнопку закрыть добавление проекта и отмена добавления проекта с переходом на мейнОкно
        self._ui.accept_button.clicked.connect(self._add_new_bot)
        self._ui.close_button.clicked.connect(self._clicked_сlose)
        self._ui.cancel_button.clicked.connect(self._clicked_сlose)

        # toDO: Добавить функцию инициализации QSS
        self._ui.background_father_widget.installEventFilter(self)
        self._ui.about_bot_edit.installEventFilter(self)
        self._ui.token_bot_edit.installEventFilter(self)
        self._ui.name_bot_edit.installEventFilter(self)
        self.installEventFilter(self)

        self.setMouseTracking(True)

        self._bot_api: Optional[IBotApi] = None
        self._bot_list: List[BotExtended] = []

    def set_all_bot(self, bot_list: List[BotExtended]):
        assert all(isinstance(bot, BotExtended) for bot in bot_list)
        self._bot_list = bot_list

    def set_bot_api(self, bot_api: IBotApi):
        self._bot_api = bot_api

    def init_placeholder_text_line(self):
        self._ui.token_bot_edit.setPlaceholderText(self._tr("Token bot"))
        self._ui.about_bot_edit.setPlaceholderText(self._tr("About bot"))

    def _init_stylesheet(self, night: bool) -> None:
        # toDO: поменять даркмод режим на изменение qssа и все qss вынести в отдельный файлпроекта или
        #  для каждого окна сделать свой первострочный инициализатор qss
        # toDO: доработать где возможно повторения
        self._ui.background_father_widget.setStyleSheet(
            self._get_group_style(StatedStylesheetEnum.MISS)
        )
        self._ui.token_bot_edit.setStyleSheet(
            self._get_line_style(StatedStylesheetEnum.MISS)
        )
        self._ui.about_bot_edit.setStyleSheet(
            self._get_line_style(StatedStylesheetEnum.MISS)
        )
        self._ui.name_bot_edit.setStyleSheet(
            self._get_line_style(StatedStylesheetEnum.MISS)
        )

    def _get_group_style(self, state: StatedStylesheetEnum) -> str:
        assert isinstance(state, StatedStylesheetEnum)
        group_style = ''
        if state == StatedStylesheetEnum.HOVER:
            group_style = (
                "QGroupBox{border: none; border-radius: 16px; background-color: " +
                BlockColorScheme.color_group_hover
                + ";}"
            )
        elif state == StatedStylesheetEnum.MISS:
            group_style = (
                "QGroupBox{border: none; border-radius: 16px; background-color: " +
                BlockColorScheme.color_group_miss
                + ";}"
            )
        return group_style

    def _get_line_style(self, state: StatedStylesheetEnum) -> str:
        assert isinstance(state, StatedStylesheetEnum)
        line_style = ''
        if state == StatedStylesheetEnum.HOVER:
            line_style = (
                "QLineEdit{border: 1px solid " + BlockColorScheme.color_line_hover + "; "
                "color: " + BlockColorScheme.color_line_hover + "; "
                "border-radius:8px; background-color: transparent;}"
            )
        elif state == StatedStylesheetEnum.MISS:
            line_style = (
                "QLineEdit{border: 1px solid " + BlockColorScheme.color_line_miss + "; "
                "color: " + BlockColorScheme.color_line_miss + "; "
                "border-radius:8px; background-color: transparent;}"
            )
        elif state == StatedStylesheetEnum.FOCUS:
            line_style = (
                "QLineEdit{border: 1px solid " + BlockColorScheme.color_line_focus + "; "
                "color: " + BlockColorScheme.color_line_focus + "; "
                "border-radius:8px; background-color: transparent;}"
            )
        elif state == StatedStylesheetEnum.NORMAL:
            line_style = (
                "QLineEdit{border: 1px solid " + BlockColorScheme.color_line_normal + "; "
                "color: " + BlockColorScheme.color_line_normal + "; "
                "border-radius:8px; background-color: transparent;}"
            )
        return line_style

    def _clicked_сlose(self):
        self.close_window.emit()

    def eventFilter(self, obj: QObject, event: QtCore.QEvent) -> bool:
        if obj == self._ui.background_father_widget:
            if event.type() == QtCore.QEvent.Type.HoverLeave:
                if self._check_lines_not_focus():
                    self._group_set_style(StatedStylesheetEnum.MISS)
            elif event.type() == QtCore.QEvent.Type.HoverEnter:
                if self._check_lines_not_focus():
                    self._group_set_style(StatedStylesheetEnum.HOVER)

        elif obj == self._ui.token_bot_edit:
            self._line_filter(event.type(), obj)
        elif obj == self._ui.about_bot_edit:
            self._line_filter(event.type(), obj)
        elif obj == self._ui.name_bot_edit:
            self._line_filter(event.type(), obj)
        return QWidget.eventFilter(self, obj, event)

    def _check_lines_not_focus(self) -> Optional[bool]:
        result = False
        if (not self._ui.about_bot_edit.hasFocus() and not self._ui.name_bot_edit.hasFocus()
                and not self._ui.token_bot_edit.hasFocus()):
            result = True
        return result

    def _line_filter(self, event: QtCore.QEvent.Type, obj: QObject) -> None:
        # toDo: Добавить typing.cast и ассерт что это qwidget
        if event == QtCore.QEvent.Type.HoverEnter and not obj.hasFocus():
            obj.setStyleSheet(self._get_line_style(StatedStylesheetEnum.HOVER))
        elif event == QtCore.QEvent.Type.HoverLeave and not obj.hasFocus():
            obj.setStyleSheet(self._get_line_style(StatedStylesheetEnum.NORMAL))
        elif event == QtCore.QEvent.Type.FocusIn:
            obj.setStyleSheet(self._get_line_style(StatedStylesheetEnum.FOCUS))
        elif event == QtCore.QEvent.Type.FocusOut:
            obj.setStyleSheet(self._get_line_style(StatedStylesheetEnum.NORMAL))

    def _group_set_style(self, state: StatedStylesheetEnum):
        self._ui.background_father_widget.setStyleSheet(self._get_group_style(state))
        if state == StatedStylesheetEnum.HOVER:
            state = StatedStylesheetEnum.NORMAL
        self._ui.token_bot_edit.setStyleSheet(self._get_line_style(state))
        self._ui.about_bot_edit.setStyleSheet(self._get_line_style(state))
        self._ui.name_bot_edit.setStyleSheet(self._get_line_style(state))

    def __get_all_bots(self) -> typing.List[BotDescription]:
        all_bots = [bot.bot_description for bot in self._bot_list]
        return all_bots

    def __get_unique_bot_name(self, base_name: str) -> str:
        used_names = [bot.bot_name for bot in self.__get_all_bots()]
        return gen_next_name(base_name, used_names)

    def _add_new_bot(self):
        try:
            name_bot = self._ui.name_bot_edit.text()
            if name_bot != '':
                self._bot_api.create_bot(
                    bot_name=self.__get_unique_bot_name(name_bot),
                    bot_token=self._ui.token_bot_edit.text(),
                    bot_description=self._ui.about_bot_edit.text()
                )
                # toDO: Перенести на кастомное диалоговое окно
                QMessageBox.information(self, 'created', 'created')
                self.new_bot_added.emit()
            else:
                # toDO: Перенести на кастомное диалоговое окно
                QMessageBox.warning(self, 'Error', self._tr('Bot name cannot be empty'))
                print(traceback.format_exc())
        except BotApiMessageException as error:
            QMessageBox.warning(self, self._tr('Error'), self._tr('Bot creation error: {0}').format(error))
            print(traceback.format_exc())

    def _tr(self, text: str) -> str:
        return tran('AddNewProjectWidget.manual', text)
