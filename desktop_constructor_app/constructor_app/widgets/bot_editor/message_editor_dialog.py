from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog

from b_logic.data_objects import BotMessage, ButtonTypesEnum
from desktop_constructor_app.constructor_app.widgets.bot_editor.ui_message_editor_dialog import Ui_MessageEditorDialog


class MessageEditorDialog(QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_MessageEditorDialog()
        self._ui.setupUi(self)

    def set_message(self, message: BotMessage):
        assert isinstance(message, BotMessage)
        self._ui.message_text_edit.setText(message.text)
        self._ui.radio_reply.setChecked(message.keyboard_type == ButtonTypesEnum.REPLY)
        self._ui.radio_inline.setChecked(message.keyboard_type == ButtonTypesEnum.INLINE)

    def message_text(self) -> str:
        return self._ui.message_text_edit.toPlainText()

    def keyboard_type(self) -> Optional[ButtonTypesEnum]:
        button_types: Optional[ButtonTypesEnum] = None
        if self._ui.radio_reply.isChecked():
            button_types = ButtonTypesEnum.REPLY
        elif self._ui.radio_inline.isChecked():
            button_types = ButtonTypesEnum.INLINE
        return button_types
