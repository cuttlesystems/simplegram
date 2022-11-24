# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtGui
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotDescription, BotMessage
from desktop_constructor_app.constructor_app.graphic_scene.bot_scene import BotScene
from desktop_constructor_app.constructor_app.properties_model import PropertiesModel, PropertyInModel
from desktop_constructor_app.constructor_app.ui_bot_editor_form import Ui_BotEditorForm


class BotEditorForm(QWidget):
    """
    Окно редактора бота
    """

    # сигнал, о том, что пользователь закрывает этот редактор
    close_bot = Signal()

    def __init__(self, parent: typing.Optional[QWidget], bot_api: IBotApi):
        super().__init__(parent)
        assert isinstance(bot_api, IBotApi)

        self._ui = Ui_BotEditorForm()
        self._ui.setupUi(self)
        self._bot_api = bot_api
        self._bot: typing.Optional[BotDescription] = None
        self._prop_model = None
        self._prop_name: typing.Optional[PropertyInModel] = None
        self._prop_token: typing.Optional[PropertyInModel] = None
        self._prop_description: typing.Optional[PropertyInModel] = None

        self._bot_scene = BotScene(self)
        self._ui.graphics_view.setScene(self._bot_scene)
        self._ui.graphics_view.setRenderHint(QPainter.Antialiasing)

        self._connect_signals()

    def set_bot(self, bot: typing.Optional[BotDescription]):
        assert isinstance(bot, BotDescription) or bot is None
        self._bot = bot

        if bot is not None:
            # todo: вот эти вещи надо будет в модель вытащить
            self._prop_name = PropertyInModel(name='Название бота', value=bot.bot_name)
            self._prop_token = PropertyInModel(name='Токен бота', value=bot.bot_token)
            self._prop_description = PropertyInModel(name='Описание', value=bot.bot_description)

            self._prop_model = PropertiesModel([
                self._prop_name,
                self._prop_token,
                self._prop_description
            ])
        else:
            self._prop_name = None
            self._prop_token = None
            self._prop_description = None

            self._prop_model = PropertiesModel([])
        self._ui.bot_params_view.setModel(self._prop_model)
        self._ui.graphics_view.centerOn(0.0, 0.0)

        self._load_bot_scene()

    def _connect_signals(self):
        self._ui.apply_button.clicked.connect(self._on_apply_button)
        self._ui.add_message_button.clicked.connect(self._on_add_message)
        self._ui.delete_message.clicked.connect(self._on_delete_message)

    def _load_bot_scene(self):
        self._bot_scene.clear_scene()
        bot_messages = self._bot_api.get_messages(self._bot)
        for message in bot_messages:
            self._bot_scene.add_message(message)

    def _upload_bot_scene(self):
        scene_messages = self._bot_scene.get_all_messages()
        for message in scene_messages:
            self._bot_api.change_message(message)

    def _on_apply_button(self, _checked: bool):
        self._save_changes()

    def _on_add_message(self, _checked: bool):
        message = self._bot_api.create_message(
            self._bot, 'Текст ботового сообщения', x=10, y=10)
        self._bot_scene.add_message(message)

    def _on_delete_message(self, _checked: bool):
        messages_for_delete = self._bot_scene.get_selected_messages()
        self._bot_scene.delete_messages(messages_for_delete)
        for message in messages_for_delete:
            self._bot_api.delete_message(message)

    def _save_changes(self):
        self._bot.bot_name = self._prop_name.value
        self._bot.bot_token = self._prop_token.value
        self._bot.bot_description = self._prop_description.value

        self._upload_bot_scene()

        self._bot_api.change_bot(self._bot)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._save_changes()
        self.close_bot.emit()
