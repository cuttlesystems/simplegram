from typing import Optional

import requests
import traceback
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QMessageBox, QMainWindow

from b_logic.bot_api.i_bot_api import BotApiException, IBotApi
from common.localisation import tran
from constructor_app.utils.get_image_from_bytes import get_pixmap_image_from_bytes
from constructor_app.widgets.selected_project_widget import DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget
from constructor_app.widgets.bot_extended import BotExtended
from network.bot_api_by_request_extended import BotApiMessageException
from constructor_app.widgets.bot_editor_widget import BotEditorWidget
from constructor_app.widgets.settings_widget import SettingsWidget


class ClientWidget(QMainWindow):

    """
    Надстройка выводимого пользователю GUI
    """

    # индекс окна логина/регистрации
    _LOGIN_INDEX_PAGE = 0
    # индекс главного окна приложения
    _MAIN_MENU_INDEX_PAGE = 1
    # индекс окна с информацией о выбранном боте
    _SELECTED_BOT_INDEX_PAGE = 2
    # инициализация окна с добавлением нового бота
    _NEW_BOT_INDEX_PAGE = 3
    # инициализация окна с редактором бота
    _BOT_REDACTOR_PAGE = 4

    # максимальное значение страниц/виджетов в стеке редактора
    _MAX_SIZE_EDITOR_STACKED_WIDGET = 1

    def __init__(self, parent: Optional[QMainWindow] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)
        self._bot_api: Optional[IBotApi] = None

        self._ui.login_page.log_in.connect(self._post_login_initial_botapi)

        self._ui.new_project_button.clicked.connect(self._start_new_project)
        self._ui.bot_list.clicked.connect(self._start_selected_project)
        self._ui.bot_new_creator_page.close_window.connect(self._start_main_menu_slot)
        self._ui.bot_new_creator_page.new_bot_added.connect(self.__load_bots_list)
        self._ui.bot_show_page.open_bot_in_redactor_signal.connect(self._start_bot_redactor)
        self._ui.bot_show_page.activated_bot_signal.connect(self.__load_bots_list)
        self._ui.log_out_button.clicked.connect(self._logout_account)
        self._ui.bot_show_page.after_remove_bot_signal.connect(self._after_remove_bot_slot)
        self._ui.bot_show_page.after_changed_bot_signal.connect(self._after_changed_bot_slot)
        # перезагрузка бот-листа при смене аватарки бота (наверное лучше не менять весь бот-лист
        # а поменять только аватарку у конкретного элемента)
        self._ui.bot_show_page.bot_avatar_changed_signal.connect(self.__load_bots_list)

        self._bot_editor = BotEditorWidget()
        self.setup_tool_stack()
        self._bot_editor.setup_tool_stack(self._ui.tool_stack)

        # первое открытие приложения, инициализация авторизации
        self._start_login_users()

        self._ui.settings_button.clicked.connect(self._start_settings_slot)

        self._bot_editor_index: Optional[int] = None
        self._settings_window = SettingsWidget()
        self._bot_editor_index = self._ui.bot_editor_stacked.addWidget(self._bot_editor)
        self._ui.bot_editor_stacked.setCurrentIndex(self._ui.bot_editor_stacked.count() - 1)

    def setup_tool_stack(self):
        self._ui.tool_stack.delete_variant_signal.connect(self._bot_editor.on_delete_variant)
        self._ui.tool_stack.mark_as_start_signal.connect(self._bot_editor.on_mark_start_button)
        self._ui.tool_stack.add_variant_signal.connect(self._bot_editor.on_add_variant_button)
        self._ui.tool_stack.mark_as_error_signal.connect(self._bot_editor.on_mark_error_button)
        self._ui.tool_stack.add_message_signal.connect(self._bot_editor.on_add_new_message)
        self._ui.tool_stack.generate_bot_signal.connect(self._bot_editor.on_generate_bot)
        self._ui.tool_stack.start_stop_bot_signal.connect(self._bot_editor.on_bot_state_changed)
        self._ui.tool_stack.read_bot_logs_signal.connect(self._bot_editor.on_read_bot_logs)
        self._ui.tool_stack.delete_message_signal.connect(self._bot_editor.on_delete_message)
        self._ui.tool_stack.unmark_as_start_signal.connect(self._bot_editor.on_unmark_start_button)
        self._ui.tool_stack.unmark_as_error_signal.connect(self._bot_editor.on_unmark_error_button)

    def _start_login_users(self) -> None:
        # выстравляю страницу инициализации
        self._ui.centrall_pannel_widget.setCurrentIndex(self._LOGIN_INDEX_PAGE)
        # toDo: Тут можно было бы доработать centrall_pannel_widget таким образом, чтобы можно было написать
        #  self._ui.centrall_pannel_widget.show_redactor_page(). А _BOT_REDACTOR_PAGE будет инкапсулирован в
        #  класс centrall_pannel_widget. Если еще centrall_pannel_widget не является кастомным типом,
        #  то про этот рефакторинг пока только в комментарии.

        # прячу сайдбар и топпанел
        self._ui.side_bar.hide()
        self._ui.top_pannel.hide()

    def _post_login_initial_botapi(self, bot_api: IBotApi) -> None:
        assert isinstance(bot_api, IBotApi)
        self._bot_api = bot_api
        self._bot_editor.set_bot_api(self._bot_api)
        self.__load_bots_list()
        self._start_main_menu()

    def _start_main_menu_slot(self) -> None:
        self._start_main_menu()

    def _start_main_menu(self) -> None:
        self._ui.centrall_pannel_widget.setCurrentIndex(self._MAIN_MENU_INDEX_PAGE)
        self._init_stylesheet_stackedwidget(0)

        self._ui.side_bar.show()
        self._ui.top_pannel.show()

        self._ui.tool_stack.hide()

    # инициализация окна с информацией о выбранном боте
    def _start_selected_project(self) -> None:
        # toDo: добавляю чистку bot_show_page

        # Set page with info about selected in sidebar bot
        self._ui.bot_show_page.set_bot_api(self._bot_api)
        self._ui.centrall_pannel_widget.setCurrentIndex(self._SELECTED_BOT_INDEX_PAGE)
        bot_extended: BotExtended = self._ui.bot_list.get_current_bot()
        assert bot_extended is not None
        bot = bot_extended

        self._ui.bot_show_page.set_bot(bot)
        self._ui.tool_stack.hide()
        # toDo: Postpone init qss in new method autoInitializeStyleSheet
        self._init_stylesheet_stackedwidget(0)

    def _start_new_project(self) -> None:
        # инициализация окна с добавлением нового бота
        # выставляю страницу добавления нового бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._NEW_BOT_INDEX_PAGE)
        self._ui.bot_new_creator_page.set_all_bot(self._ui.bot_list.get_bots())
        self._ui.bot_new_creator_page.set_bot_api(self._bot_api)
        self._ui.tool_stack.hide()
        # настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(1)

    def _logout_account(self) -> None:
        # toDO: добавить реализацию выхода для сервера
        self._start_login_users()

    def _start_settings_slot(self, _toggled: bool) -> None:
        self._settings_window.show()

    def _start_bot_redactor(self) -> None:
        try:
            self._ui.centrall_pannel_widget.setCurrentIndex(self._BOT_REDACTOR_PAGE)
            self._ui.tool_stack.show()

            self._init_stylesheet_stackedwidget(0)

            bot_extended = self._ui.bot_list.get_current_bot()
            assert bot_extended is not None

            bot_id = bot_extended.bot_description.id
            bot = self._bot_api.get_bot_by_id(bot_id)

            self._ui.tool_stack.set_switch_toggle(bot_extended.bot_state)
            self._bot_editor.update_state_bot.connect(self.__load_bots_list)
            self._bot_editor.set_bot(bot)
            print('Open bot with Name: "{name}" and Id:"{id}"'.format(name=str(bot.bot_name), id=str(bot.id)))

        except requests.exceptions.ConnectionError as e:
            # toDo: add translate kz, ru
            QMessageBox.warning(self, self._tr('Error'), self._tr('Connection error: {0}').format(e))
            print(traceback.format_exc())
        except BotApiMessageException as exception:
            QMessageBox.warning(self, self._tr('Error'), str(exception))
            print(traceback.format_exc())

    def _init_stylesheet_stackedwidget(self, state: int) -> None:
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный инициализатор
        #  qss, доработать функцию изменения nightMode/darkMode и функцию состояния stackedwidget при выбранном окне
        if state == 0:
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(241,241,241);}")
        else:
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(105,105,109);}")

    def __load_bots_list(self):
        # toDo:Add method-handler state item in sidebar
        # toDo:Recode item in sidebar
        try:
            # получение всех ботов юзера из БД
            bots = self._bot_api.get_bots()
            self._ui.bot_list.set_current_bot()
            self._ui.bot_list.clear()

            # получение списка запущенных ботов
            running_bots = self._bot_api.get_running_bots_info()
            for bot in bots:
                if bot.id in running_bots:
                    bot_state = True
                else:
                    bot_state = False
                # toDo: Add icons initialization
                if bot.bot_profile_photo is not None:
                    image_data = self._bot_api.get_image_data_by_url(bot.bot_profile_photo)
                    bot_icon = get_pixmap_image_from_bytes(image_data)
                else:
                    bot_icon = QPixmap(DEFAULT_BOT_AVATAR_ICON_RESOURCE_PATH)
                self._ui.bot_list.add_bot(
                    BotExtended(
                        bot_icon=bot_icon,
                        bot_description=bot,
                        bot_state=bot_state))
            self._ui.bot_list.update_current()
        except BotApiException as error:
            QMessageBox.warning(self, self._tr('Error'), str(error))

    def _after_remove_bot_slot(self) -> None:
        self.__load_bots_list()
        self._start_main_menu()

    def _after_changed_bot_slot(self) -> None:
        self.__load_bots_list()

    def _tr(self, text: str) -> str:
        return tran('ClientWidget.manual', text)

