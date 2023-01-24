import urllib.request
from typing import Optional
from urllib.error import HTTPError

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QDialog

from b_logic.data_objects import BotMessage, ButtonTypesEnum
from constructor_app.widgets.bot_editor.ui_message_editor_dialog import Ui_MessageEditorDialog


class MessageEditorDialog(QDialog):
    _IMAGE_HEIGHT = 130
    _IMAGE_NOT_FOUND_WINDOW_HEIGHT = 130
    _IMAGE_NOT_FOUND_WINDOW_WIDTH = 130

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

    def show_image(self, message: BotMessage):
        assert isinstance(message, BotMessage)
        if message.photo:
            try:
                url = message.photo
                image_data = urllib.request.urlopen(url).read()
                image = QtGui.QImage()
                image.loadFromData(image_data)
                image_size_ratio = self._IMAGE_HEIGHT / image.height()
                self._ui.message_image.setFixedHeight(self._IMAGE_HEIGHT)
                self._ui.message_image.setFixedWidth(int(image.width() * image_size_ratio))
                self._ui.message_image.setPixmap(QtGui.QPixmap(image))
            except HTTPError as error:
                print(f'------------------->logging. Image not found! {error}')
                self._ui.message_image.setFixedSize(
                    self._IMAGE_NOT_FOUND_WINDOW_WIDTH, self._IMAGE_NOT_FOUND_WINDOW_HEIGHT)
                self._ui.message_image.setText('Error!\nImage not found.')
                self._ui.message_image.setAlignment(QtCore.Qt.AlignCenter)
        else:
            self._ui.message_image.setFixedSize(
                self._IMAGE_NOT_FOUND_WINDOW_WIDTH, self._IMAGE_NOT_FOUND_WINDOW_HEIGHT)
            self._ui.message_image.setText('Image not set.')
            self._ui.message_image.setAlignment(QtCore.Qt.AlignCenter)
