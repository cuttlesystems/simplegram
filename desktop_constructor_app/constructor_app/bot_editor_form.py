# This Python file uses the following encoding: utf-8
import typing

import PySide6
from PySide6 import QtGui
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.ui_bot_editor_form import Ui_BotEditorForm


class BotEditorForm(QWidget):
    close_bot = Signal()

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApi):
        super().__init__(parent)
        self._ui = Ui_BotEditorForm()
        self._ui.setupUi(self)
        self._bot_api = bot_api
        self._bot: typing.Optional[BotDescription] = None
        self._connect_signals()

    def set_bot(self, bot: typing.Optional[BotDescription]):
        assert isinstance(bot, BotDescription) or bot is None
        self._bot = bot
        if bot is not None:
            self._ui.token_line_edit.setText(bot.bot_token)
            self._ui.bot_name_line_edit.setText(bot.bot_name)
            self._ui.descrtiption_text_edit.setText(bot.bot_description)
        else:
            self._ui.token_line_edit.setText('')
            self._ui.bot_name_line_edit.setText('')
            self._ui.descrtiption_text_edit.setText('')

    def _connect_signals(self):
        self._ui.apply_button.clicked.connect(self._on_apply_button)

    def _on_apply_button(self, _checked: bool):
        self._bot.bot_name = self._ui.bot_name_line_edit.text()
        self._bot.bot_token = self._ui.token_line_edit.text()
        self._bot.bot_description = self._ui.descrtiption_text_edit.text()
        self._bot_api.change_bot(self._bot)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.close_bot.emit()
