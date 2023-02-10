from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Slot, Signal

from b_logic.utils.image_to_bytes import get_binary_data_from_image_file
from common.localisation import tran
from constructor_app.utils.get_image_from_bytes import get_pixmap_image_from_bytes

from constructor_app.widgets.ui_selected_project_widget import Ui_SelectedProjectWidget
from b_logic.bot_api.i_bot_api import BotDescription, IBotApi

DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH: str = ":icons/widgets/times_icon/newProject.png"


class SelectedProjectWidget(QWidget):

    activated_bot_signal = Signal(bool)
    open_bot_in_redactor_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)
        self._ui = Ui_SelectedProjectWidget()
        self._ui.setupUi(self)
        self._ui.switch_activated_bot.clicked.connect(self._switch_bot)
        self._ui.open_in_redactor_button.clicked.connect(self.__bot_editing)
        self._init_StyleSheet()
        self._bot_api: Optional[IBotApi] = None
        self._bot: Optional[BotDescription] = None

    def _init_StyleSheet(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss
        self._ui.groupBox.setStyleSheet("QGroupBox{border-radius:22px; border:none; "
                                        "background-color:rgb(255,255,255);}")
        self._ui.open_in_redactor_button.setStyleSheet("QPushButton{background-color:rgb(57,178,146);border:none;"
                                                       "color:white;border-radius:8px;}")

    def _switch_bot(self):
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный
        #  инициализатор qss и продумать грамотный флаг состояния бота
        if(self._ui.switch_activated_bot.isChecked()):
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#4DAAFF;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is enabled"))
            self.activated_bot_signal.emit(True)
        else:
            self._ui.marker_state_bot.setStyleSheet(
                "QLabel{border-radius:8px; border:none; color:white;"
                "background-color:#FF5F8F;}")
            self._ui.marker_state_bot.setText(self._tr(u"Bot is disabled"))
            self.activated_bot_signal.emit(False)

    def set_bot(self, bot: BotDescription, bot_state: bool) -> None:
        # Set name bot in lineEdit
        assert isinstance(bot, BotDescription)
        assert isinstance(bot_state, bool)
        self._bot = bot

        # Установка дефолтной аватарки бота или фотки из БД, если есть.
        if bot.bot_profile_photo is not None:
            image_data: Optional[bytes] = self._bot_api.get_image_data_by_url(bot.bot_profile_photo)
            image: Optional[QPixmap] = get_pixmap_image_from_bytes(image_data)
            self._ui.icon_bot_button.setIcon(image)
        else:
            self._ui.icon_bot_button.setIcon(QPixmap(DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH))

        self._ui.name_bot_edit.setText(bot.bot_name)
        self._ui.switch_activated_bot.setChecked(bot_state)
        self._switch_bot()

    def set_bot_api(self, bot_api: IBotApi):
        self._bot_api = bot_api

    def __bot_editing(self) -> None:
        # коннект кнопки открытия бота в редакторе и сигналом старта редактирования в основном клиент/менеджерном
        # приложении
        self.open_bot_in_redactor_signal.emit()

    def _tr(self, text: str) -> str:
        return tran('SelectedProjectWidget.manual', text)
