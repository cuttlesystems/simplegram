# This Python file uses the following encoding: utf-8
import typing

from PySide6.QtWidgets import QWidget

from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.ui_bot_editor_form import Ui_BotEditorForm


class BotEditorForm(QWidget):
    def __init__(self, parent: typing.Optional[QWidget]):
        super().__init__(parent)
        self._ui = Ui_BotEditorForm()
        self._ui.setupUi(self)
        self._connect_signals()

    def set_bot(self, bot: BotDescription):
        assert isinstance(bot, BotDescription)
        self._ui.token_line_edit.setText(bot.bot_token)

    def _connect_signals(self):
        pass
