import typing

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QPainter
from constructor_app.widgets.ui_selected_project_widget import Ui_SelectedProjectWidget

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypesEnum
from common.localisation import tran
from common.model_property import ModelProperty
from constructor_app.graphic_scene.bot_scene import BotScene
from constructor_app.widgets.bot_properties_model import BotPropertiesModel


class SelectedProjectWidget(QWidget):

    _bot: BotDescription
    _bot_api: IBotApi
    _bot_scene: BotScene

    activated_bot_signal = Signal(bool)
    open_bot_in_redactor_signal = Signal()

    def __init__(self, parent: typing.Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)
        self._ui = Ui_SelectedProjectWidget()
        self._ui.setupUi(self)
        self._ui.switch_activated_bot.clicked.connect(self._switch_bot)
        self._ui.open_in_redactor_button.clicked.connect(self.__bot_editing)
        self._init_StyleSheet()

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
        #self._bot_scene.clear_scene()
        self._ui.name_bot_edit.setText(bot.bot_name)
        self._ui.switch_activated_bot.setChecked(bot_state)
        self._switch_bot()

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

        self._load_bot_scene()

    def __bot_editing(self) -> None:
        # коннект кнопки открытия бота в редакторе и сигналом старта редактирования в основном клиент/менеджерном
        # приложении
        self.open_bot_in_redactor_signal.emit()

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
