import os.path
from enum import Enum
from typing import Optional

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog, QFileDialog

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotMessage, ButtonTypesEnum, MessageTypeEnum, BotDescription
from constructor_app.widgets.bot_editor.ui_message_editor_dialog import Ui_MessageEditorDialog
from b_logic.utils.image_to_bytes import get_binary_data_from_file


class MessageMediaFileState(Enum):
    LOADED = 'loaded'
    DELETED = 'deleted'
    NO_ACTION = 'no_action'


class MessageEditorDialog(QDialog):
    _IMAGE_HEIGHT = 130
    _IMAGE_WIDTH = 130
    _IMAGE_NOT_FOUND_WINDOW_HEIGHT = 130
    _IMAGE_NOT_FOUND_WINDOW_WIDTH = 130
    _IMAGE_ALLOWED_FORMATS = '(*.png *.bmp *.jpg *.gif *.ico *.jpeg *.svg *.tif *.webp *.xpm)'
    _VIDEO_ALLOWED_FORMATS = '(*.mp4 *.mov *.wmv *.avi *.webm *.mkv)'

    def __init__(self, bot_api: IBotApi, bot: BotDescription, parent: Optional[QtWidgets.QWidget] = None):
        assert isinstance(bot_api, IBotApi)
        assert isinstance(bot, BotDescription)
        assert isinstance(parent, Optional[QtWidgets.QWidget])
        super().__init__(parent)

        self._ui = Ui_MessageEditorDialog()
        self._ui.setupUi(self)

        self._bot_api = bot_api
        self._bot = bot

        self._ui.load_image_button.clicked.connect(self._on_load_image)
        self._ui.remove_image_button.clicked.connect(self._on_remove_image)

        self._ui.load_video_button.clicked.connect(self._on_load_video)
        self._ui.remove_video_button.clicked.connect(self._on_remove_video)

        self._message_image_path: Optional[str] = None
        self._message_image_state: MessageMediaFileState = MessageMediaFileState.NO_ACTION

        self._message_video_path: Optional[str] = None
        self._message_video_state: MessageMediaFileState = MessageMediaFileState.NO_ACTION

    def set_message(self, message: BotMessage) -> None:
        assert isinstance(message, BotMessage)
        self._ui.message_text_edit.setText(message.text)

        # задаем тип кнопок для вариантов
        self._ui.radio_reply.setChecked(message.keyboard_type == ButtonTypesEnum.REPLY)
        self._ui.radio_inline.setChecked(message.keyboard_type == ButtonTypesEnum.INLINE)

        # отображаем изображение для сообщения
        self._ui.message_image_label.clear()
        if message.photo:
            self._show_image(self._bot_api.get_image_data_by_url(message.photo))
        if message.video:
            self._ui.message_video_label.setText('Video file is attached')

        # задаем тип сообщения
        self._ui.message_variants_radio.setChecked(message.message_type == MessageTypeEnum.VARIANTS)
        self._ui.message_any_input_radio.setChecked(message.message_type == MessageTypeEnum.ANY_INPUT)
        self._ui.message_jump_radio.setChecked(message.message_type == MessageTypeEnum.GOTO)

        # задаем имя переменной для считывания данных от пользователя
        self._ui.variable_name_line_edit.setText(message.variable)

        self._ui.next_message_list_widget.set_messages(self._bot_api.get_messages(self._bot))
        self._ui.next_message_list_widget.set_selected_message(message.next_message_id)

    def get_message_text(self) -> str:
        return self._ui.message_text_edit.toPlainText()

    def get_keyboard_type(self) -> Optional[ButtonTypesEnum]:
        button_types: Optional[ButtonTypesEnum] = None
        if self._ui.radio_reply.isChecked():
            button_types = ButtonTypesEnum.REPLY
        elif self._ui.radio_inline.isChecked():
            button_types = ButtonTypesEnum.INLINE
        return button_types

    def get_message_type(self) -> MessageTypeEnum:
        if self._ui.message_variants_radio.isChecked():
            message_type = MessageTypeEnum.VARIANTS
        elif self._ui.message_any_input_radio.isChecked():
            message_type = MessageTypeEnum.ANY_INPUT
        elif self._ui.message_jump_radio.isChecked():
            message_type = MessageTypeEnum.GOTO
        else:
            raise ValueError('Message type undefined')
        return message_type

    def get_variable_name(self) -> Optional[str]:
        variable = self._ui.variable_name_line_edit.text()
        return variable

    def get_next_message(self) -> Optional[BotMessage]:
        return self._ui.next_message_list_widget.get_selected_message()

    def _show_image(self, image_data: Optional[bytes]) -> None:
        assert isinstance(image_data, Optional[bytes])
        if image_data is not None:
            image = QtGui.QImage()
            image.loadFromData(image_data)
            image_size = self._calculate_optimal_image_size(image.width(), image.height())
            self._ui.message_image_label.setFixedWidth(image_size.width())
            self._ui.message_image_label.setFixedHeight(image_size.height())
            self._ui.message_image_label.setPixmap(QtGui.QPixmap(image))
        else:
            self._ui.message_image_label.setFixedSize(
                self._IMAGE_NOT_FOUND_WINDOW_WIDTH, self._IMAGE_NOT_FOUND_WINDOW_HEIGHT)
            self._ui.message_image_label.setStyleSheet("border: 1px solid #cecdd1;")
            self._ui.message_image_label.setText('Error!\nImage not found')
            self._ui.message_image_label.setAlignment(QtCore.Qt.AlignCenter)

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

    def _on_load_image(self, checked: bool) -> None:
        file_info = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            dir='',
            filter=f'Images {self._IMAGE_ALLOWED_FORMATS};;All files (*.*)'
        )
        print(file_info)
        if len(file_info[0]) > 0:
            full_path_to_file: str = file_info[0]
            image_data = get_binary_data_from_file(full_path_to_file)
            self._show_image(image_data)
            self._message_image_path = full_path_to_file
            self._message_image_state = MessageMediaFileState.LOADED

    def _on_load_video(self, checked: bool) -> None:
        file_info = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            dir='',
            filter=f'Videos {self._VIDEO_ALLOWED_FORMATS};;All files (*.*)'
        )
        print(file_info)
        if len(file_info[0]) > 0:
            full_path_to_file: str = file_info[0]
            self._video_must_be_removed_state = False
            self._message_video_path = full_path_to_file
            self._message_video_state = MessageMediaFileState.LOADED
            self._ui.message_video_label.setText('Video file is attached')

    def _on_remove_image(self, checked: bool) -> None:
        self._ui.message_image_label.clear()
        self._message_image_path = None
        self._message_image_state = MessageMediaFileState.DELETED

    def _on_remove_video(self, checked: bool) -> None:
        self._message_video_path = None
        self._message_video_state = MessageMediaFileState.DELETED
        self._ui.message_video_label.setText('Video file is not attached')

    def get_message_image_path(self) -> Optional[str]:
        return self._message_image_path

    def get_message_image_state(self) -> MessageMediaFileState:
        return self._message_image_state

    def get_message_video_path(self) -> Optional[str]:
        return self._message_video_path

    def get_message_video_state(self) -> MessageMediaFileState:
        return self._message_video_state
