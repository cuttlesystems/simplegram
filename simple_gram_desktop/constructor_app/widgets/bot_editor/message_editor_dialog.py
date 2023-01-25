from typing import Optional

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotMessage, ButtonTypesEnum
from constructor_app.widgets.bot_editor.ui_message_editor_dialog import Ui_MessageEditorDialog


class MessageEditorDialog(QDialog):
    _IMAGE_HEIGHT = 130
    _IMAGE_WIDTH = 130
    _IMAGE_NOT_FOUND_WINDOW_HEIGHT = 130
    _IMAGE_NOT_FOUND_WINDOW_WIDTH = 130

    def __init__(self, bot_api: IBotApi, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self._ui = Ui_MessageEditorDialog()
        self._ui.setupUi(self)
        self._bot_api = bot_api

    def set_message(self, message: BotMessage):
        assert isinstance(message, BotMessage)
        self._ui.message_text_edit.setText(message.text)
        self._ui.radio_reply.setChecked(message.keyboard_type == ButtonTypesEnum.REPLY)
        self._ui.radio_inline.setChecked(message.keyboard_type == ButtonTypesEnum.INLINE)
        self._ui.message_image.clear()
        if message.photo:
            self._show_image(self._bot_api.get_message_image_by_url(message))

    def message_text(self) -> str:
        return self._ui.message_text_edit.toPlainText()

    def keyboard_type(self) -> Optional[ButtonTypesEnum]:
        button_types: Optional[ButtonTypesEnum] = None
        if self._ui.radio_reply.isChecked():
            button_types = ButtonTypesEnum.REPLY
        elif self._ui.radio_inline.isChecked():
            button_types = ButtonTypesEnum.INLINE
        return button_types

    def _show_image(self, image_data: Optional[bytes]) -> None:
        assert isinstance(image_data, Optional[bytes])
        if image_data is not None:
            image = QtGui.QImage()
            image.loadFromData(image_data)
            image_size = self._calculate_optimal_image_size(image.width(), image.height())
            self._ui.message_image.setFixedWidth(image_size.width())
            self._ui.message_image.setFixedHeight(image_size.height())
            self._ui.message_image.setPixmap(QtGui.QPixmap(image))
        else:
            self._ui.message_image.setFixedSize(
                self._IMAGE_NOT_FOUND_WINDOW_WIDTH, self._IMAGE_NOT_FOUND_WINDOW_HEIGHT)
            self._ui.message_image.setStyleSheet("border: 1px solid #cecdd1;")
            self._ui.message_image.setText('Error!\nImage not found')
            self._ui.message_image.setAlignment(QtCore.Qt.AlignCenter)

    def _calculate_optimal_image_size(self, width: int, height: int) -> QSize:
        assert isinstance(height, int)
        assert isinstance(width, int)
        size = QSize()
        if height > width:
            image_size_ratio = self._IMAGE_HEIGHT / height
            size.setWidth(int(width * image_size_ratio))
            size.setHeight(self._IMAGE_HEIGHT)
        else:
            image_size_ratio = self._IMAGE_WIDTH / width
            size.setWidth(self._IMAGE_WIDTH)
            size.setHeight(int(height * image_size_ratio))
        return size
