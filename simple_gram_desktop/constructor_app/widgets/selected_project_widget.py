import os
from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QPainter

from b_logic.utils.image_to_bytes import get_binary_data_from_image_file
from common.localisation import tran
from constructor_app.utils.get_image_from_bytes import get_pixmap_image_from_bytes

from constructor_app.widgets.ui_selected_project_widget import Ui_SelectedProjectWidget

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypesEnum
from common.localisation import tran
from common.model_property import ModelProperty
from constructor_app.graphic_scene.bot_scene import BotScene
from constructor_app.widgets.bot_properties_model import BotPropertiesModel

from b_logic.bot_api.i_bot_api import BotDescription, IBotApi

DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH: str = ":icons/widgets/times_icon/newProject.png"


class SelectedProjectWidget(QWidget):
    _IMAGE_ALLOWED_FORMATS = '(*.png *.bmp *.jpg *.gif *.ico *.jpeg *.tif *.webp *.xpm)'

    activated_bot_signal = Signal()
    open_bot_in_redactor_signal = Signal()
    bot_avatar_changed_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)
        self._ui = Ui_SelectedProjectWidget()
        self._ui.setupUi(self)
        self._ui.switch_activated_bot.clicked.connect(self._switch_bot)
        self._ui.open_in_redactor_button.clicked.connect(self.__bot_editing)
        self._ui.icon_bot_button.clicked.connect(self._set_bot_image)
        self._init_StyleSheet()
        self._bot_api: Optional[IBotApi] = None
        self._bot: Optional[BotDescription] = None
        self._bot_scene: Optional[BotScene] = None


    def _init_StyleSheet(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss
        self._ui.background.setStyleSheet("QGroupBox{border-radius:22px; border:none; "
                                        "background-color:rgb(255,255,255);}")
        self._ui.open_in_redactor_button.setStyleSheet("QPushButton{background-color:rgb(57,178,146);border:none;"
                                                       "color:white;border-radius:8px;}")

    def _switch_bot(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss и продумать грамотный флаг состояния бота
        if self._ui.switch_activated_bot.isChecked():
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#4DAAFF;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is enabled"))
            self._bot_api.start_bot(self._bot)
            self.activated_bot_signal.emit()
        else:
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#FF5F8F;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is disabled"))
            self._bot_api.stop_bot(self._bot)
            self.activated_bot_signal.emit()

    def _init_state_bot(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss и продумать грамотный флаг состояния бота
        if self._ui.switch_activated_bot.isChecked():
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#4DAAFF;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is enabled"))
        else:
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#FF5F8F;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is disabled"))

    def set_bot(self, bot: BotDescription, bot_state: bool) -> None:
        # Set name bot in lineEdit
        assert isinstance(bot, BotDescription)
        assert isinstance(bot_state, bool)
        self._bot = bot

        # Установка дефолтной аватарки бота или фотки из БД, если есть.
        if self._bot.bot_profile_photo is not None:
            image_data: Optional[bytes] = self._bot_api.get_image_data_by_url(self._bot.bot_profile_photo)
            image: Optional[QPixmap] = get_pixmap_image_from_bytes(image_data)
            self._ui.icon_bot_button.setIcon(image)
        else:
            self._ui.icon_bot_button.setIcon(QPixmap(DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH))

        self._ui.name_bot_edit.setText(self._bot.bot_name)
        #self._bot_scene.clear_scene()
        self._ui.name_bot_edit.setText(bot.bot_name)
        self._ui.switch_activated_bot.setChecked(bot_state)
        self._init_state_bot()

    def set_bot_api(self, bot_api: IBotApi):
        self._bot_api = bot_api

        assert isinstance(bot, BotDescription) or bot is None
        self._init_preview_bot()
        self._bot = self._bot_api.get_bot_by_id(bot_id=bot.id, with_link=1)
        self._bot_scene.set_bot_scene(self._bot)

        self._prop_model = BotPropertiesModel()

        if bot is not None:
            self._prop_model.set_name(self._bot.bot_name)
            self._prop_model.set_token(self._bot.bot_token)
            self._prop_model.set_description(self._bot.bot_description)
            self._prop_model.set_link(self._bot.bot_link)

        else:
            self._prop_model.set_name('')
            self._prop_model.set_token('')
            self._prop_model.set_description('')
            self._prop_model.set_link('')

        self._bot_api.generate_bot(self._bot)
        self._load_bot_scene()

    def __bot_editing(self) -> None:
        # коннект кнопки открытия бота в редакторе и сигналом старта редактирования в основном клиент/менеджерном
        # приложении
        self.open_bot_in_redactor_signal.emit()

    def _set_bot_image(self, checked: bool) -> None:
        file_info = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            dir='',
            filter=f'Images {self._IMAGE_ALLOWED_FORMATS};;All files (*.*)'
        )
        if len(file_info[0]) > 0:
            full_path_to_file: str = file_info[0]
            self._ui.icon_bot_button.setIcon(QPixmap(full_path_to_file))

            # Обновляем объект бота на сервере, добавляем аватарку.
            self._bot.bot_profile_photo = full_path_to_file
            self._bot.profile_photo_filename = os.path.basename(full_path_to_file)
            self._bot_api.change_bot(self._bot)

            # обновляем информацию о боте для корректного отображения картинки
            self._bot = self._bot_api.get_bot_by_id(self._bot.id)

            # отправляем сигнал на обновление бот_листа
            self.bot_avatar_changed_signal.emit()

    def _load_bot_scene(self):
        self._bot_scene.clear_scene()
        bot_messages = self._bot_api.get_messages(self._bot)
        for message in bot_messages:
            variants = self._bot_api.get_variants(message)
            self._bot_scene.add_message(message, variants)

    def set_bot_api(self, bot_api: IBotApi):
        assert isinstance(bot_api, IBotApi)
        self._bot_api = bot_api

    def _init_preview_bot(self) -> None:

        # toDo: Подумать и переделать подгрузку скрина бот-сцены на
        self._bot: typing.Optional[BotDescription] = None
        self._prop_name: typing.Optional[ModelProperty] = None
        self._prop_token: typing.Optional[ModelProperty] = None
        self._prop_description: typing.Optional[ModelProperty] = None

        self._bot_scene = BotScene(self)
        self._ui.bot_view.setScene(self._bot_scene)
        self._ui.bot_view.setRenderHint(QPainter.Antialiasing)

        scene_rect = self._bot_scene.itemsBoundingRect()
        self._ui.bot_view.centerOn(scene_rect.x(), scene_rect.y())

    def _tr(self, text: str) -> str:
        return tran('SelectedProjectWidget.manual', text)
