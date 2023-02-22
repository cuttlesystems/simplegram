import os, traceback

from PySide6 import QtCore
from typing import Optional

from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, QUrl, QObject

from constructor_app.utils.get_image_from_bytes import get_pixmap_image_from_bytes
from constructor_app.widgets.bot_extended import BotExtended
from constructor_app.widgets.qss.label_qss import LabelColorScheme

from constructor_app.widgets.ui_selected_project_widget import Ui_SelectedProjectWidget

from common.localisation import tran
from constructor_app.graphic_scene.bot_scene import BotScene

from b_logic.bot_api.i_bot_api import BotDescription, IBotApi
from network.bot_api_by_request_extended import BotApiMessageException

DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH: str = ":icons/widgets/times_icon/new_bot.png"


class SelectedProjectWidget(QWidget):
    _IMAGE_ALLOWED_FORMATS = '(*.png *.bmp *.jpg *.gif *.ico *.jpeg *.tif *.webp *.xpm)'

    activated_bot_signal = Signal()
    open_bot_in_redactor_signal = Signal()
    bot_avatar_changed_signal = Signal()
    after_remove_bot_signal = Signal()
    after_changed_bot_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)
        self._ui = Ui_SelectedProjectWidget()
        self._ui.setupUi(self)
        self._ui.switch_activated_bot.clicked.connect(self._switch_bot)
        self._ui.open_in_redactor_button.clicked.connect(self.__bot_editing)
        self._ui.icon_bot_button.clicked.connect(self._set_bot_image)
        self._ui.open_file_button.clicked.connect(self._set_bot_image)
        self._ui.reset_icon_button.clicked.connect(self._on_reset_icon_button)
        self._ui.edit_bot_button.clicked.connect(self._changed_bot)
        self._ui.remove_bot_button.clicked.connect(self._remove_bot)
        self._init_StyleSheet()
        self._bot_api: Optional[IBotApi] = None
        self._bot: Optional[BotDescription] = None
        self._bot_scene: Optional[BotScene] = None
        self._ui.link_bot_header.setOpenExternalLinks(True)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self._ui.link_bot_label.installEventFilter(self)
        self._ui.link_bot_label.setMouseTracking(True)

    def eventFilter(self, obj: QObject, event: QtCore.QEvent) -> bool:
        if obj == self._ui.link_bot_label:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                open_link = QDesktopServices()
                link = self._bot.bot_link
                open_link.openUrl(QUrl(link))
        return False

    def _init_StyleSheet(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss
        #self._ui.background.setStyleSheet(
        #    "QGroupBox{border-radius:22px; border:none; "
        #    "background-color:rgba(23,23,23,220);}")
        #self._ui.open_in_redactor_button.setStyleSheet(
        #    "QPushButton{background-color:rgb(57,178,146);border:none;"
        #    "color:white;border-radius:8px;}")
        pass

    def _switch_bot(self, toggled: bool):
        bot_enabled_state = toggled
        if toggled:
            try:
                self._bot_api.start_bot(self._bot)
                self._ui.marker_state_bot.setStyleSheet(
                    LabelColorScheme.enabled)
                self._ui.marker_state_bot.setText(self._tr("Bot is enabled"))
                bot_enabled_state = True
            except BotApiMessageException as error:
                QMessageBox(self, 'Error', str(error))
                print(traceback.format_exc())
                bot_enabled_state = False
        else:
            self._ui.marker_state_bot.setStyleSheet(
                LabelColorScheme.disabled)
            self._ui.marker_state_bot.setText(self._tr("Bot is disabled"))
            try:
                self._bot_api.stop_bot(self._bot)
                bot_enabled_state = False
            except BotApiMessageException as error:
                QMessageBox(self, 'Error', str(error))
                print(traceback.format_exc())
                bot_enabled_state = False

        self._ui.switch_activated_bot.blockSignals(True)
        try:
            self._ui.switch_activated_bot.setChecked(bot_enabled_state)
            self.activated_bot_signal.emit()
        finally:
            self._ui.switch_activated_bot.blockSignals(False)

    def _init_state_bot(self):
        if self._ui.switch_activated_bot.isChecked():
            self._ui.marker_state_bot.setStyleSheet(
                LabelColorScheme.enabled)
            self._ui.marker_state_bot.setText(self._tr("Bot is enabled"))
        else:
            self._ui.marker_state_bot.setStyleSheet(
                LabelColorScheme.disabled)
            self._ui.marker_state_bot.setText(self._tr("Bot is disabled"))

    def set_bot(self, bot: BotExtended) -> None:
        assert isinstance(bot, BotExtended)
        try:
            # обновляем информацию о боте для корректного отображения картинки
            self._bot = self._bot_api.get_bot_by_id(bot_id=bot.bot_description.id, with_link=1)

            # Установка дефолтной аватарки бота или фотки из БД, если есть.
            # toDo: Добавить функцию инициализации иконки из стартерпака иконок заказанных у дизайнера
            if self._bot.bot_profile_photo is not None:
                image_data: Optional[bytes] = self._bot_api.get_image_data_by_url(self._bot.bot_profile_photo)
                image: Optional[QPixmap] = get_pixmap_image_from_bytes(image_data)
                self._ui.icon_bot_button.setIcon(image)
            else:
                self._ui.icon_bot_button.setIcon(QPixmap(DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH))

            self._ui.switch_activated_bot.setChecked(bot.bot_state)
            self._init_state_bot()

            self._ui.name_bot_edit.setText(self._bot.bot_name)
            self._ui.description_bot_edit.setText(self._bot.bot_description)
            if self._bot.bot_link != 'Bot token is not specified.':
                font = self._ui.link_bot_label.font()
                font.setUnderline(True)
                self._ui.link_bot_label.setFont(font)
                self._ui.link_bot_label.setText(self._bot.bot_link)
            else:
                font = self._ui.link_bot_label.font()
                font.setUnderline(False)
                self._ui.link_bot_label.setFont(font)
                self._ui.link_bot_label.setText('The link for bot will be generated after the bot is generated')
                self._ui.link_bot_label.setDisabled(True)
            self._ui.token_bot_edit.setText(self._bot.bot_token)

        except BotApiMessageException as error:
            QMessageBox(self, self._tr('Error'), str(error))
            print(traceback.format_exc())

    def __bot_editing(self) -> None:
        # коннект кнопки открытия бота в редакторе и сигналом старта редактирования в основном клиент/менеджерном
        # приложении
        self.open_bot_in_redactor_signal.emit()

    def _set_bot_image(self, checked: bool) -> None:
        file_info = QFileDialog.getOpenFileName(
            parent=self,
            caption=self._tr('Open file'),
            dir='',
            filter=self._tr('Images {0};;All files (*.*)').format(self._IMAGE_ALLOWED_FORMATS)
        )
        if len(file_info[0]) > 0:
            full_path_to_file: str = file_info[0]
            self._ui.icon_bot_button.setIcon(QPixmap(full_path_to_file))

            # Обновляем объект бота на сервере, добавляем аватарку.
            self._bot.bot_profile_photo = full_path_to_file
            self._bot.profile_photo_filename = os.path.basename(full_path_to_file)
            self._bot_api.change_bot(self._bot)

            # отправляем сигнал на обновление бот_листа
            self.bot_avatar_changed_signal.emit()

    def set_bot_api(self, bot_api: IBotApi):
        assert isinstance(bot_api, IBotApi)
        self._bot_api = bot_api

    def _remove_bot(self) -> None:
        self._bot_api.delete_bot(self._bot.id)
        self._bot = None
        self.after_remove_bot_signal.emit()

    def _changed_bot(self) -> None:
        new_name_bot = self._ui.name_bot_edit.text()
        self._bot.bot_name = new_name_bot
        new_description_bot = self._ui.description_bot_edit.text()
        self._bot.bot_description = new_description_bot
        new_token_bot = self._ui.token_bot_edit.text()
        self._bot.bot_token = new_token_bot
        self._bot_api.change_bot(self._bot)
        self.after_changed_bot_signal.emit()

    def _on_reset_icon_button(self) -> None:
        self._ui.icon_bot_button.setIcon(QPixmap(DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH))
        self._bot_api.remove_bot_image(self._bot)

        self.bot_avatar_changed_signal.emit()

    def _on_open_file_button(self) -> None:
        pass

    def _tr(self, text: str) -> str:
        return tran('SelectedProjectWidget.manual', text)
