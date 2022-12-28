# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtGui import QPainter, QAction
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox, QMainWindow

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypes
from desktop_constructor_app.common.localisation import tran
from desktop_constructor_app.common.utils.name_utils import gen_next_name
from desktop_constructor_app.constructor_app.graphic_scene.bot_scene import BotScene
from desktop_constructor_app.common.model_property import ModelProperty
from desktop_constructor_app.constructor_app.graphic_scene.block_graphics_item import BlockGraphicsItem
from desktop_constructor_app.constructor_app.widgets.bot_properties_model import BotPropertiesModel
from desktop_constructor_app.constructor_app.widgets.bot_editor.message_editor_dialog import MessageEditorDialog
from desktop_constructor_app.constructor_app.widgets.bot_editor.ui_bot_editor_form import Ui_BotEditorForm
from desktop_constructor_app.constructor_app.widgets.bot_editor.variant_editor_dialog import VariantEditorDialog


class BotEditorForm(QMainWindow):
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
        self._prop_name: typing.Optional[ModelProperty] = None
        self._prop_token: typing.Optional[ModelProperty] = None
        self._prop_description: typing.Optional[ModelProperty] = None

        self._bot_scene = BotScene(self)
        self._ui.graphics_view.setScene(self._bot_scene)
        self._ui.graphics_view.setRenderHint(QPainter.Antialiasing)

        self._prop_model = BotPropertiesModel()
        self._ui.bot_params_view.setModel(self._prop_model)

        self._connect_signals()

    def set_bot(self, bot: typing.Optional[BotDescription]):
        assert isinstance(bot, BotDescription) or bot is None
        self._bot = bot

        if bot is not None:
            self._prop_model.set_name(bot.bot_name)
            self._prop_model.set_token(bot.bot_token)
            self._prop_model.set_description(bot.bot_description)
        else:
            self._prop_model.set_name('')
            self._prop_model.set_token('')
            self._prop_model.set_description('')

        self._load_bot_scene()

        self._actual_actions_state()

        self._ui.splitter.setSizes([200, 600])

        QtCore.QTimer.singleShot(0, self._on_after_set_bot)

    def _on_after_set_bot(self):
        # небольшое обходное решение, чтобы произвести центрирование области
        scene_rect = self._bot_scene.itemsBoundingRect()
        self._ui.graphics_view.centerOn(scene_rect.x(), scene_rect.y())

    def _connect_signals(self):
        self._ui.action_add_message.triggered.connect(self._on_add_new_message)
        self._ui.action_add_variant.triggered.connect(self._on_action_add_variant)
        self._ui.action_delete_message.triggered.connect(self._on_delete_message)
        self._ui.action_generate_bot.triggered.connect(self._on_generate_bot)
        self._ui.action_start_bot.triggered.connect(self._on_start_bot)
        self._ui.action_stop_bot.triggered.connect(self._on_stop_bot)
        self._ui.action_mark_start.triggered.connect(self._on_mark_as_start_button)
        self._ui.action_delete_variant.triggered.connect(self._on_delete_variant)

        self._ui.action_manual_save.triggered.connect(self._on_apply_button)

        # сигналы, которые испускает сцена подключаем через QtCore.Qt.ConnectionType.QueuedConnection
        # (чтобы завершился обработчик клика)
        self._bot_scene.request_add_new_variant.connect(
            self._on_bot_scene_add_new_variant, QtCore.Qt.ConnectionType.QueuedConnection)

        self._bot_scene.request_change_message.connect(
            self._on_change_message, QtCore.Qt.ConnectionType.QueuedConnection)

        self._bot_scene.request_change_variant.connect(
            self._on_change_variant, QtCore.Qt.ConnectionType.QueuedConnection)

        self._bot_scene.selection_changed.connect(self._on_selection_changed)

    def _load_bot_scene(self):
        self._bot_scene.clear_scene()
        bot_messages = self._bot_api.get_messages(self._bot)
        for message in bot_messages:
            variants = self._bot_api.get_variants(message)
            self._bot_scene.add_message(message, variants)

    def _upload_bot_scene(self):
        scene_messages = self._bot_scene.get_all_messages()
        for message in scene_messages:
            self._bot_api.change_message(message)

    def _on_apply_button(self, _checked: bool):
        self._save_changes()

    def _on_add_new_message(self, _checked: bool):
        message = self._bot_api.create_message(
            self._bot, 'Текст ботового сообщения', ButtonTypes.REPLY, x=10, y=10)
        self._bot_scene.add_message(message, [])
        self._actual_actions_state()

    def _add_variant(self):
        selected_blocks = self._bot_scene.get_selected_blocks_graphics()
        if len(selected_blocks) == 1:
            selected_block = selected_blocks[0]
            variants = selected_block.get_variants()
            message = selected_block.get_message()

            # тут изменение сообщения, чтобы предыдущие правки по сообщению отправились на сервер
            # (не потерялись изменения)
            self._bot_api.change_message(message)

            variant_name = self._generate_unique_variant_name('New bot variant', variants)
            self._bot_api.create_variant(message, variant_name)
            messages = self._bot_api.get_messages(self._bot)
            # todo: этот момент можно оптимизировать и переписать лучше
            updated_message = next(mes for mes in messages if mes.id == message.id)
            updated_variants = self._bot_api.get_variants(updated_message)
            print('delete message', message)
            self._bot_scene.delete_messages([message])
            graphics_item = self._bot_scene.add_message(updated_message, updated_variants)
            print('add variant for message: ', message.text)
            print('graphics_item sceneBoundingRect {0}'.format(graphics_item.sceneBoundingRect()))
            self._bot_scene.update(graphics_item.sceneBoundingRect())
        else:
            QMessageBox.warning(
                self,
                self._tr('Error'),
                self._tr('Please select only one block for add variant')
            )

        self._actual_actions_state()

    def _on_action_add_variant(self, _toggled: bool):
        self._add_variant()

    def _on_bot_scene_add_new_variant(self, _message: BotMessage, _variants: typing.List[BotVariant]):
        self._add_variant()

    def _on_change_message(self, block: BlockGraphicsItem, variants: typing.List[BotVariant]):
        assert isinstance(block, BlockGraphicsItem)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        message = block.get_message()
        editor_dialog = MessageEditorDialog(self)
        editor_dialog.set_message(block.get_message())

        # todo: тут появляется побочный эффект - после закрытия окна диалога следующий клик пропадает,
        #  надо бы поправить

        if editor_dialog.exec_() == QDialog.DialogCode.Accepted:
            message.text = editor_dialog.message_text()
            message.keyboard_type = editor_dialog.keyboard_type()
            self._bot_api.change_message(message)

            block.change_message(message)

    def _on_change_variant(self, block_graphics_item: BlockGraphicsItem, variant: BotVariant):
        assert isinstance(block_graphics_item, BlockGraphicsItem)
        assert isinstance(variant, BotVariant)
        variant_editor_dialog = VariantEditorDialog(self)
        messages = self._bot_scene.get_all_messages()
        variant_editor_dialog.set_dialog_data(variant, messages)
        if variant_editor_dialog.exec_() == QDialog.DialogCode.Accepted:
            variant = variant_editor_dialog.get_variant()
            self._bot_api.change_variant(variant)
            block_graphics_item.change_variant(variant)

    def _on_delete_variant(self, _checked: bool):
        deleted_variant: typing.Optional[BotVariant] = None
        block_with_deleted_variant: typing.Optional[BlockGraphicsItem] = None
        block_graphics = self._bot_scene.get_selected_blocks_graphics()
        for block in block_graphics:
            deleted_variant = block.get_current_variant()
            if deleted_variant is not None:
                block_with_deleted_variant = block
                break

        if deleted_variant is not None:
            self._bot_api.delete_variant(deleted_variant)
            block_with_deleted_variant.delete_variant(deleted_variant.id)

        self._actual_actions_state()

    def _on_mark_as_start_button(self, _checked: bool):
        selected_messages = self._bot_scene.get_selected_messages()
        selected_messages_number = len(selected_messages)
        if selected_messages_number == 1:
            selected_message = selected_messages[0]
            self._bot_api.set_bot_start_message(self._bot, selected_message)
        else:
            QMessageBox.warning(self, 'Error', 'Select only one message to set is as start message')

    def _generate_unique_variant_name(self, variant_name: str, variants: typing.List[BotVariant]) -> str:
        assert isinstance(variant_name, str)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        names = [variant.text for variant in variants]
        return gen_next_name(variant_name, names)

    def _on_delete_message(self, _checked: bool):
        messages_for_delete = self._bot_scene.get_selected_messages()
        self._bot_scene.delete_messages(messages_for_delete)
        for message in messages_for_delete:
            self._bot_api.delete_message(message)

        self._actual_actions_state()

    def _on_generate_bot(self, _checked: bool):
        try:
            self._save_changes()
            self._bot_api.generate_bot(self._bot)
        except Exception as e:
            self._process_exception(e)

    def _on_start_bot(self, _checked: bool):
        try:
            self._bot_api.start_bot(self._bot)
        except Exception as e:
            self._process_exception(e)

    def _on_stop_bot(self, _checked: bool):
        try:
            self._bot_api.stop_bot(self._bot)
        except Exception as e:
            self._process_exception(e)

    def _process_exception(self, exception: Exception):
        if not isinstance(exception, NotImplementedError):
            exception_mes = str(exception)
            print(exception_mes)
            QMessageBox.warning(self, 'Error', exception_mes)
        else:
            raise

    def _save_changes(self):
        self._bot.bot_name = self._prop_model.get_name()
        self._bot.bot_token = self._prop_model.get_token()
        self._bot.bot_description = self._prop_model.get_description()

        self._upload_bot_scene()

        self._bot_api.change_bot(self._bot)

    def _on_selection_changed(self):
        self._actual_actions_state()

    def _actual_actions_state(self):
        """
        Перевести действия в актуальное состояние в зависимости от текущих выделенных элементов.
        Часть элементов меню и кнопок на панели инструментов станет активной или неактивной,
        в зависимости от текущего состояния сцены (что выделено или не выделено)
        """
        blocks_graphics = self._bot_scene.get_selected_blocks_graphics()
        selected_blocks_number = len(blocks_graphics)
        is_selected_blocks = selected_blocks_number > 0
        one_selected_block = selected_blocks_number == 1
        selected_variant = False
        if one_selected_block:
            selected_variant = blocks_graphics[0].get_current_variant() is not None

        self._ui.action_delete_message.setEnabled(is_selected_blocks)
        self._ui.action_delete_variant.setEnabled(selected_variant)
        self._ui.action_mark_start.setEnabled(one_selected_block)
        self._ui.action_add_variant.setEnabled(one_selected_block)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._save_changes()
        self.close_bot.emit()

    def _tr(self, text: str):
        return tran('BotEditorForm', text)
