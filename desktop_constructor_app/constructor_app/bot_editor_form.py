# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtGui
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.bot_scene import BotScene
from desktop_constructor_app.constructor_app.properties_model import PropertiesModel, PropertyInModel
from desktop_constructor_app.constructor_app.ui_bot_editor_form import Ui_BotEditorForm


class BotEditorForm(QWidget):
    """
    Окно редактора бота
    """

    # сигнал, о том, что пользователь закрывает этот редактор
    close_bot = Signal()

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApi):
        super().__init__(parent)
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

        self._connect_signals()

    def set_bot(self, bot: typing.Optional[BotDescription]):
        assert isinstance(bot, BotDescription) or bot is None
        self._bot = bot

        if bot is not None:
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

    def _connect_signals(self):
        self._ui.apply_button.clicked.connect(self._on_apply_button)
        self._ui.add_message_button.clicked.connect(self._on_add_message)

    def _on_apply_button(self, _checked: bool):
        self._save_changes()

    def _on_add_message(self, _checked: bool):
        self._bot_scene.add_message(10, 10)

    def _save_changes(self):
        self._bot.bot_name = self._prop_name.value
        self._bot.bot_token = self._prop_token.value
        self._bot.bot_description = self._prop_description.value

        self._bot_api.change_bot(self._bot)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._save_changes()
        self.close_bot.emit()
