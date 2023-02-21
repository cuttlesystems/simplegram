# This Python file uses the following encoding: utf-8
import typing

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Signal, QPointF, QRect
from PySide6.QtGui import QPainter, QBrush, QColor, QAction
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox, QMainWindow, QMenu

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypesEnum
from common.localisation import tran
from common.model_property import ModelProperty
from constructor_app.widgets.tool_stack_widget import ToolStackWidget
from utils.name_utils import gen_next_name
from constructor_app.graphic_scene.block_graphics_item import BlockGraphicsItem
from constructor_app.graphic_scene.bot_scene import BotScene
from constructor_app.widgets.bot_editor.message_editor_dialog import MessageEditorDialog
from constructor_app.widgets.ui_bot_editor_widget import Ui_BotEditorWidget
from constructor_app.widgets.bot_editor.variant_editor_dialog import VariantEditorDialog
from constructor_app.widgets.bot_properties_model import BotPropertiesModel

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests


class BotEditorWidget(QWidget):
    """
    Окно редактора бота
    """

    # сигнал, о том, что пользователь закрывает этот редактор
    close_bot = Signal()
    update_state_bot = Signal()

    delete_message_setEnabled = Signal(bool)
    delete_variant_setEnabled = Signal(bool)
    mark_start_setEnabled = Signal(bool)
    mark_error_setEnabled = Signal(bool)
    add_variant_setEnabled = Signal(bool)

    def __init__(self, parent: typing.Optional[QWidget] = None):
        # toDo: срастить extendedовское определение бота с текущим редактором и убрать botApi как входной параметр
        super().__init__(parent)

        self._ui = Ui_BotEditorWidget()
        self._ui.setupUi(self)
        self._bot_api: typing.Optional[IBotApi] = None
        self._bot: typing.Optional[BotDescription] = None
        self._prop_name: typing.Optional[ModelProperty] = None
        self._prop_token: typing.Optional[ModelProperty] = None
        self._prop_description: typing.Optional[ModelProperty] = None

        self._bot_scene = BotScene(self)

        self._tool_stack_widget: typing.Optional[ToolStackWidget] = None

        self._ui.graphics_view.setScene(self._bot_scene)
        self._ui.graphics_view.setRenderHint(QPainter.Antialiasing)

        self._prop_model = BotPropertiesModel()
        self._ui.bot_params_view.setModel(self._prop_model)
        self._prop_model.set_allow_edit(False)

        self._connect_signals()

        self._menu_block = QMenu(self)
        self._menu_scheme = QMenu(self)

        self._add_message_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/add_message.png'), self._tr('Add message'), self)
        self._add_message_action.triggered.connect(self._on_add_new_message_action)
        self._delete_message_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/delete_message.png'), self._tr('Delete message'), self)
        self._delete_message_action.triggered.connect(self._on_delete_message_action)
        self._add_variant_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/add_variant.png'), self._tr('Add variant'), self)
        self._add_variant_action.triggered.connect(self._on_add_variant_action)
        self._mark_start_message_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/first_message.png'), self._tr('Mark start message'), self)
        self._mark_start_message_action.triggered.connect(self._mark_start_action)
        self._mark_error_message_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/error_message.png'), self._tr('Mark error message'), self)
        self._mark_error_message_action.triggered.connect(self._on_mark_error_action)
        self._start_bot_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/start_bot.png'), self._tr('Start bot'), self)
        self._start_bot_action.triggered.connect(self._on_start_bot_action)
        self._stop_bot_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/stop_bot.png'), self._tr('Stop bot'), self)
        self._stop_bot_action.triggered.connect(self._on_stop_bot_action)
        self._generate_bot_action = \
            QAction(QtGui.QIcon(':icons/images/generate.svg'), self._tr('Generate bot'), self)
        self._generate_bot_action.triggered.connect(self._on_generate_bot_action)
        self._show_logs_action = \
            QAction(QtGui.QIcon(':icons/widgets/times_icon/logs.png'), self._tr('Show log'), self)
        self._show_logs_action.triggered.connect(self._on_read_bot_logs_action)

        self._menu_block.addActions([self._add_message_action, self._delete_message_action])
        self._menu_block.addSeparator()
        self._menu_block.addAction(self._add_variant_action)
        self._menu_block.addSeparator()
        self._menu_block.addActions([self._mark_start_message_action, self._mark_error_message_action])
        self._menu_block.addSeparator()
        self._menu_block.addActions([self._start_bot_action, self._stop_bot_action, self._generate_bot_action])

        self._menu_scheme.addAction(self._add_message_action)
        self._menu_scheme.addSeparator()
        self._menu_scheme.addActions([self._start_bot_action, self._stop_bot_action, self._generate_bot_action])
        self._menu_scheme.addSeparator()
        self._menu_scheme.addAction(self._show_logs_action)

        self._prepare_and_setup_context_menu()

    def set_bot_api(self, bot_api: IBotApi):
        # toDo: добавить заполнение через IBotApi
        assert isinstance(bot_api, IBotApi)
        self._bot_api = bot_api

    def set_bot(self, bot: typing.Optional[BotDescription]):
        assert isinstance(bot, BotDescription) or bot is None
        self._bot = self._bot_api.get_bot_by_id(bot_id=bot.id, with_link=1)
        self._bot_scene.set_bot_scene(self._bot)

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

        self._actual_actions_state()

        self._ui.stdout_textedit.clear()
        self._ui.stderr_textedit.clear()

        self._ui.splitter.setSizes([200, 600])

        QtCore.QTimer.singleShot(0, self._on_after_set_bot)

    def _on_after_set_bot(self):
        # небольшое обходное решение, чтобы произвести центрирование области
        scene_rect = self._bot_scene.itemsBoundingRect()
        self._ui.graphics_view.centerOn(scene_rect.x(), scene_rect.y())

    def _connect_signals(self):
        # сигналы, которые испускает сцена подключаем через QtCore.Qt.ConnectionType.QueuedConnection
        # (чтобы завершился обработчик клика)
        self._bot_scene.request_add_new_variant.connect(
            self._on_bot_scene_add_new_variant)

        self._bot_scene.request_change_message.connect(
            self._on_change_message)

        self._bot_scene.request_change_variant.connect(
            self._on_change_variant)

        self._bot_scene.selection_changed.connect(self._on_selection_changed)

    def _prepare_and_setup_context_menu(self) -> None:
        """
        Создать, подготовить и установить контекстное меню для блока и пустой области
        """
        self._ui.graphics_view.setup_block_menu(self._menu_block)
#
        self._ui.graphics_view.setup_empty_menu(self._menu_scheme)

    def _load_bot_scene(self):
        self._bot_scene.clear_scene()
        bot_messages = self._bot_api.get_messages(self._bot)
        for message in bot_messages:
            variants = self._bot_api.get_variants(message)
            self._bot_scene.add_message(message, variants)

    def _on_generate_bot_action(self, triggered: bool):
        self.__generate_bot()

    def _on_generate_bot(self):
        self.__generate_bot()

    def __generate_bot(self):
        try:
            self._save_changes()
            self._bot_api.generate_bot(self._bot)
        except Exception as e:
            self._process_exception(e)

    def _on_read_bot_logs_action(self, triggered: bool):
        self.__read_bot_logs()

    def _on_read_bot_logs(self) -> None:
        self.__read_bot_logs()

    def __read_bot_logs(self) -> None:
        bot_logs = self._bot_api.get_bot_logs(self._bot)
        stderr_text = ''.join(bot_logs.stderr_lines)
        stdout_text = ''.join(bot_logs.stdout_lines)
        self._ui.stdout_textedit.setText(stdout_text)
        self._ui.stderr_textedit.setText(stderr_text)

    def _upload_bot_scene(self):
        """Сохраняет изменения по всем сообщениям бота, в БД."""
        scene_messages = self._bot_scene.get_all_messages()
        for message in scene_messages:
            self._bot_api.change_message(message)

    def on_apply_button(self) -> None:
        self._save_changes()

    def _add_new_message(self, position: QPointF) -> None:
        assert isinstance(position, QPointF)
        messages = self._bot_api.get_messages(self._bot)
        message_name = self._generate_unique_message_name(self._tr('New bot message'), messages)
        message = self._bot_api.create_message(
            self._bot, message_name, ButtonTypesEnum.REPLY, x=position.x(), y=position.y())
        self._bot_scene.add_message(message, [])
        self._actual_actions_state()

    def _generate_unique_variant_name(self, variant_name: str, variants: typing.List[BotVariant]) -> str:
        assert isinstance(variant_name, str)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        names = [variant.text for variant in variants]
        return gen_next_name(variant_name, names)

    def _generate_unique_message_name(self, message_name: str, messages: typing.List[BotMessage]) -> str:
        assert isinstance(message_name, str)
        assert all(isinstance(message, BotMessage) for message in messages)
        names = [message.text for message in messages]
        return gen_next_name(message_name, names)

    def _add_variant(self) -> None:
        selected_blocks = self._bot_scene.get_selected_blocks_graphics()
        # добавление варианта возможно только тогда, когда выбран один блок
        if len(selected_blocks) == 1:
            selected_block = selected_blocks[0]
            # получим сообщение и варианты выбранного блока
            message = selected_block.get_message()
            variants = selected_block.get_variants()

            # сгенерируем уникальное имя для нового варианта
            variant_name = self._generate_unique_variant_name(self._tr('New bot variant'), variants)

            # создадим вариант на сервере
            variant = self._bot_api.create_variant(message, variant_name)

            # добавим созданный вариант в графический блок сцены
            selected_block.add_variant(variant)
        else:
            QMessageBox.warning(
                self,
                self._tr('Error'),
                self._tr('Please select only one block for add variant')
            )

        self._actual_actions_state()

    def _on_add_variant_button(self):
        self._add_variant()

    def _on_add_variant_action(self):
        self._add_variant()

    def _on_bot_scene_add_new_variant(self, _message: BotMessage, _variants: typing.List[BotVariant]):
        self._add_variant()

    def _on_change_message(self, block: BlockGraphicsItem, variants: typing.List[BotVariant]):
        assert isinstance(block, BlockGraphicsItem)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        message = block.get_message()
        message = self._bot_api.get_one_message(message.id)
        editor_dialog = MessageEditorDialog(self._bot_api, self._bot, self)
        editor_dialog.set_message(message)

        # todo: тут появляется побочный эффект - после закрытия окна диалога следующий клик пропадает,
        #  надо бы поправить

        if editor_dialog.exec_() == QDialog.DialogCode.Accepted:
            message.text = editor_dialog.get_message_text()
            message.keyboard_type = editor_dialog.get_keyboard_type()
            message.variable = editor_dialog.get_variable_name()
            message.message_type = editor_dialog.get_message_type()

            next_message = editor_dialog.get_next_message()
            message.next_message_id = next_message.id if next_message is not None else None
            print(f'Удаляем имэйдж? {editor_dialog.get_image_must_be_removed_state()}')
            if editor_dialog.get_image_must_be_removed_state():
                self._bot_api.remove_message_image(message)
            message.photo = editor_dialog.get_message_image_path()
            message.photo_filename = editor_dialog.get_message_image_filename()
            self._bot_api.change_message(message)

            block.change_message(message)

    def _on_change_variant(self, block_graphics_item: BlockGraphicsItem, variant: BotVariant):
        assert isinstance(block_graphics_item, BlockGraphicsItem)
        assert isinstance(variant, BotVariant)
        variant_editor_dialog = VariantEditorDialog(self)
        messages = self._bot_scene.get_all_messages()
        variant_editor_dialog.set_dialog_data(variant, messages)
        if variant_editor_dialog.exec_() == QDialog.DialogCode.Accepted:
            try:
                variant = variant_editor_dialog.get_variant()
                self._bot_api.change_variant(variant)
                block_graphics_item.change_variant(variant)
            except BotApiException as exception:
                QMessageBox.warning(
                    self,
                    self._tr('Error'),
                    self._tr('Variant changing error: {0}').format(str(exception))
                )

    def _on_start_bot_action(self):
        self._tool_stack_widget.init_switch_toggle(True)
        self.__start_bot()

    def _on_start_bot(self):
        self.__start_bot()

    def __start_bot(self):
        try:
            self._bot_api.start_bot(self._bot)
            self.update_state_bot.emit()
        except Exception as e:
            self._process_exception(e)

    def _on_stop_bot_action(self):
        self._tool_stack_widget.init_switch_toggle(False)
        self.__stop_bot()

    def _on_stop_bot(self):
        self.__stop_bot()

    def __stop_bot(self):
        try:
            self._bot_api.stop_bot(self._bot)
            self.update_state_bot.emit()
        except Exception as e:
            self._process_exception(e)

    def _on_delete_message_action(self):
        self.__delete_message()

    def _on_delete_message(self):
        self.__delete_message()

    def __delete_message(self):
        messages_for_delete = self._bot_scene.get_selected_messages()
        self._bot_scene.delete_messages(messages_for_delete)
        for message in messages_for_delete:
            self._bot_api.delete_message(message)

        self._actual_actions_state()

    def _on_mark_error_action(self, triggered: bool) -> None:
        self.__mark_as_error()

    def _on_mark_error_button(self) -> None:
        self.__mark_as_error()

    def __mark_as_error(self) -> None:
        selected_messages = self._bot_scene.get_selected_messages()
        selected_messages_number = len(selected_messages)
        if selected_messages_number == 1:
            selected_message = selected_messages[0]
            self._bot_api.set_bot_error_message(self._bot, selected_message)

            updated_bot_info = self._bot_api.get_bot_by_id(self._bot.id)
            self._bot_scene.set_bot_scene(updated_bot_info)
            self._bot = updated_bot_info
            self._upload_bot_scene()

            self._load_bot_scene()
            selected_block = self._bot_scene.get_block_by_message_id(selected_message.id)
            if selected_block is not None:
                selected_block.setSelected(True)
            self._actual_actions_state()
        else:
            QMessageBox.warning(
                self,
                self._tr('Error'),
                self._tr('Select only one message to set as error message'))

    def _on_delete_variant(self):
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

    def _mark_start_action(self, triggered: bool) -> None:
        self.__mark_as_start()

    def setup_tool_stack(self, tool: ToolStackWidget):
        self._tool_stack_widget = tool

    def _on_mark_start_button(self) -> None:
        self.__mark_as_start()

    def __mark_as_start(self) -> None:
        selected_messages = self._bot_scene.get_selected_messages()
        selected_messages_number = len(selected_messages)
        if selected_messages_number == 1:
            selected_message = selected_messages[0]
            self._bot_api.set_bot_start_message(self._bot, selected_message)

            updated_bot_info = self._bot_api.get_bot_by_id(self._bot.id)
            self._bot_scene.set_bot_scene(updated_bot_info)
            self._bot = updated_bot_info
            self._upload_bot_scene()

            self._load_bot_scene()
            selected_block = self._bot_scene.get_block_by_message_id(selected_message.id)
            if selected_block is not None:
                selected_block.setSelected(True)
            self._actual_actions_state()
        else:
            QMessageBox.warning(
                self,
                self._tr('Error'),
                self._tr('Select only one message to set as start message'))

    def _on_add_new_message_action(self, triggered: bool) -> None:
        self.__add_new_message()

    def _on_add_new_message(self) -> None:
        self.__add_new_message()

    def __add_new_message(self) -> None:
        position = self._ui.graphics_view.get_context_menu_position()
        # действие вызвано не через контекстное меню
        if position is None:
            # координаты нового сообщения: по центру видимой области редактора
            actual_position = self._ui.graphics_view.mapToScene(self._ui.graphics_view.get_central_point())
        else:
            # координаты нового сообщения: где было показано контекстное меню
            actual_position = self._ui.graphics_view.mapToScene(position)
        self._add_new_message(actual_position)

    def _process_exception(self, exception: Exception):
        if not isinstance(exception, NotImplementedError):
            exception_mes = str(exception)
            print(exception_mes)
            QMessageBox.warning(self, 'Error', exception_mes)
        else:
            raise

    def _save_changes(self):
        # освежим объект бота с сервера
        self._bot = self._bot_api.get_bot_by_id(self._bot.id)

        # запишем текущие поля из интерфейса пользователя в объект бота
        self._bot.bot_name = self._prop_model.get_name()
        self._bot.bot_token = self._prop_model.get_token()
        self._bot.bot_description = self._prop_model.get_description()

        # отправим актуальный объект бота обратно на сервер
        self._bot_api.change_bot(self._bot)

        # отправляем все объекты сообщений на сервер
        self._upload_bot_scene()

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

        self._tool_stack_widget.set_delete_message_enabled(is_selected_blocks)
        self._tool_stack_widget.set_delete_variant_enabled(selected_variant)
        self._tool_stack_widget.set_mark_start_enabled(one_selected_block)
        self._tool_stack_widget.set_mark_error_enabled(one_selected_block)
        self._tool_stack_widget.set_add_variant_enabled(one_selected_block)

    def forced_close_bot(self) -> None:
        self._save_changes()
        self.close_bot.emit()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self._save_changes()
        self.close_bot.emit()

    def _tr(self, text: str) -> str:
        return tran('BotEditorForm.manual', text)
