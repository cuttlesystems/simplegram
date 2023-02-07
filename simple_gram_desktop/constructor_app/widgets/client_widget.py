from typing import Optional

import requests
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide6 import QtGui
from PySide6.QtCore import Signal, SLOT


from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import BotApiException, IBotApi, GetBotListException
from common.localisation import tran

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget
from constructor_app.widgets.bot_editor.bot_editor_form import BotEditorForm
from constructor_app.widgets.bot_list_widget import BotExtended
from network.bot_api_by_request_extended import BotApiMessageException


class ClientWidget(QWidget):

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

    selected_bot_id = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)
        self._bot_api: Optional[IBotApi] = None

        # дружу кнопку ентера при авторизации и инициализации мейн окна
        self._ui.login_page.log_in.connect(self._post_login_initial_botapi)

        #self._ui.bot_new_creator_page.close_window.connect(self._start_main_menu)

        """Сайдбар"""
        # дружу кнопку нового проекта и инициализацию окна создания бота
        self._ui.new_project_button.clicked.connect(self._start_new_project)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.bot_list.clicked.connect(self._start_selected_project)
        self._ui.bot_list.clicked.connect(self._start_selected_project)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        #self._ui.logo_block.clicked.connect(self._start_main_menu)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.bot_show_page.open_bot_in_redactor_signal.connect(self._start_bot_redactor)

        # первое открытие приложения, инициализация авторизации
        self._start_login_users()

        #self.user

    # инициализация окна авторизации
    def _start_login_users(self) -> None:
        # выстравляю страницу инициализации
        self._ui.centrall_pannel_widget.setCurrentIndex(self._LOGIN_INDEX_PAGE)
        # toDo: Тут можно было бы доработать centrall_pannel_widget таким образом, чтобы можно было написать
        #  self._ui.centrall_pannel_widget.show_redactor_page(). А _BOT_REDACTOR_PAGE будет инкапсулирован в
        #  класс centrall_pannel_widget. Если еще centrall_pannel_widget не является кастомным типом,
        #  то про этот рефакторинг пока только в todo можем написать.


        # прячу сайдбар и топпанел
        self._ui.side_bar.hide()
        self._ui.top_pannel.hide()

    def _post_login_initial_botapi(self, bot_api: IBotApi) -> None:
        assert isinstance(bot_api, IBotApi)
        self._bot_api = bot_api
        self.__load_bots_list()
        self._start_main_menu()

    #инициализация основого окна приложения
    def _start_main_menu(self) -> None:
        #выстравляю страницу главного окна
        self._ui.centrall_pannel_widget.setCurrentIndex(self._MAIN_MENU_INDEX_PAGE)
        self._init_stylesheet_stackedwidget(0)
        # показываю сайдбар и топпанел
        self._ui.side_bar.show()
        self._ui.top_pannel.show()
        self._ui.tool_stack.hide()

    # инициализация окна с информацией о выбранном боте
    def _start_selected_project(self) -> None:
        # Set page with info about selected in sidebar bot
        self._ui.centrall_pannel_widget.setCurrentIndex(self._SELECTED_BOT_INDEX_PAGE)
        bot = self._ui.bot_list.get_current_bot().bot_description  # get BotExtended
        bot_state = self._ui.bot_list.get_current_bot().bot_state
        # toDo: Refactoring set_bot(botExtended)
        self._ui.bot_show_page.set_bot(bot, bot_state)
        self._ui.tool_stack.hide()
        # toDo: Postpone init qss in new method autoInitializeStyleSheet
        self._init_stylesheet_stackedwidget(0)

    def _start_new_project(self) -> None:
        # инициализация окна с добавлением нового бота
        # выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._NEW_BOT_INDEX_PAGE)
        self._ui.tool_stack.hide()
        # настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(1)

    def _start_bot_redactor(self) -> None:
        try:
            # выстравляю страницу добавления новго бота
            self._ui.centrall_pannel_widget.setCurrentIndex(self._BOT_REDACTOR_PAGE)
            self._ui.tool_stack.show()
            # настраиваю таблицу стилей подложки
            self._init_stylesheet_stackedwidget(0)

            bot_id = self._ui.bot_list.get_current_bot().bot_description.id + 30303030
            bot = self._bot_api.get_bot_by_id(bot_id)
            self._ui.bot_redactor_page.set_bot_api(self._bot_api)
            self._ui.bot_redactor_page.setup_tool_stack(self._ui.tool_stack)
            self._ui.bot_redactor_page.set_bot(bot)
        except requests.exceptions.ConnectionError as e:
            # toDo: add translate kz, ru
            QMessageBox.warning(self, self._tr('Error'), self._tr('Connection error: {0}').format(e))
        except BotApiMessageException as exception:
            QMessageBox.warning(self, self._tr('Error'), str(exception))

    def _init_stylesheet_stackedwidget(self, state: int) -> None:
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный инициализатор
        #  qss, доработать функцию изменения nightMode/darkMode и функцию состояния stackedwidget при выбранном окне
        if state == 0:
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(241,241,241);}")
        else:
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(105,105,109);}")

    def _tr(self, text: str) -> str:
        return tran('ClientWidget.manual', text)

    def __load_bots_list(self):
        # toDo:Add method-handler state item in sidebar
        # toDo:Recode item in sidebar
        try:
            # получение всех ботов юзера из БД
            bots = self._bot_api.get_bots()
            self._ui.bot_list.clear()
            # получение списка запущенных ботов
            running_bots = self._bot_api.get_running_bots_info()
            for bot in bots:
                if bot.id in running_bots:
                    bot_state = True
                else:
                    bot_state = False
                # toDo: Add icons initialization
                self._ui.bot_list.add_bot(
                    BotExtended(
                        bot_icon=QtGui.QPixmap(":/icons/widgets/times_icon/newProject.png"),
                        bot_description=bot,
                        bot_state=bot_state))
        except BotApiException as error:
            QMessageBox.warning(self, self._tr('Error'), str(error))
