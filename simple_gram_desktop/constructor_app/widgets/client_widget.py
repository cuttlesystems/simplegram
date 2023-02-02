import typing

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT

from b_logic.bot_api.i_bot_api import BotApiException
from common.localisation import tran

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget

class ClientWidget(QWidget):

    """
    Надстройка выводимого пользователю GUI
    """
    _LIST_DATA_ROLE = QtCore.Qt.UserRole + 1

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

    def __init__(self, parent: typing.Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)
        self._bot_api = None

        #дружу кнопку ентера при авторизации и инициализации мейн окна
        self._ui.loginWindow.log_in.connect(self._start_main_menu)
        #дружу
        self._ui.botNewCreator.close_window.connect(self._start_main_menu)

        """Сайдбар"""
        #дружу кнопку нового проекта и инициализацию окна создания бота
        self._ui.new_project_button.clicked.connect(self._start_new_project)
        #дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.bot_list.clicked.connect(self._start_selected_project)
        #дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.logo_block.clicked.connect(self._start_main_menu)
        #дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.botShowWindow.open_bot_in_redactor_signal.connect(self._start_bot_redactor)

        #первое открытие приложения, инициализация авторизации
        self._start_login_users()

    #инициализация окна авторизации
    def _start_login_users(self) ->None:
        #выстравляю страницу инициализации
        self._ui.centrall_pannel_widget.setCurrentIndex(self._LOGIN_INDEX_PAGE)
        # прячу сайдбар и топпанел
        self._ui.side_bar.hide()
        self._ui.top_pannel.hide()

    #инициализация основого окна приложения
    def _start_main_menu(self, bot_api) ->None:
        self._bot_api = bot_api
        #выстравляю страницу главного окна
        self._ui.centrall_pannel_widget.setCurrentIndex(self._MAIN_MENU_INDEX_PAGE)
        self._init_stylesheet_stackedwidget(0)
        #показываю сайдбар и топпанел
        self._ui.side_bar.show()
        self._ui.top_pannel.show()
        self._init_projectslist()
        self.__load_bots_list()

    # инициализация окна с информацией о выбранном боте
    def _start_selected_project(self) ->None:
        #выстравляю страницу с информацией о выбранном боте
        self._ui.centrall_pannel_widget.setCurrentIndex(self._SELECTED_BOT_INDEX_PAGE)
        self._init_stylesheet_stackedwidget(0)

    # инициализация окна с добавлением нового бота
    def _start_new_project(self) ->None:
        #выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._NEW_BOT_INDEX_PAGE)
        #настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(1)

    def _start_bot_redactor(self) ->None:
        #выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._BOT_REDACTOR_PAGE)
        #настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(0)

    def _init_stylesheet_stackedwidget(self, state: int) -> None:
        # toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный инициализатор
        #  qss, доработать функцию изменения nightMode/darkMode и функцию состояния stackedwidget при выбранном окне
        if (state == 0):
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(241,241,241);}")
        else:
            self._ui.centrall_pannel_widget.setStyleSheet(
                "QStackedWidget{border: none;background: rgb(105,105,109);}")

    def _init_projectslist(self) -> None:
        #toDo: Добавить подгрузку списка проектов с сервера
        self._ui.bot_list.add_bot(QPixmap(":/icons/widgets/times_icon/newProject.png"), "BotNew", False, 0)

    def _tr(self, text: str) -> str:
        return tran('ClientWidget.manual', text)

    def __load_bots_list(self):
        try:
            bots = self._bot_api.get_bots()
            bot_items = []
            self._ui.bot_list.clear()

            running_bots = self._bot_api.get_running_bots_info()
            running_bot_background_color = self.palette().linkVisited()
            for bot in bots:
                bot_item = QListWidgetItem(bot.bot_name)
                if bot.id in running_bots:
                    bot_item.setBackground(running_bot_background_color)
                    bot_item.setText(f'{bot.bot_name} --> running')
                bot_item.setData(self._LIST_DATA_ROLE, bot)
                bot_items.append(bot_item)
                self._ui.bot_list.addItem(bot_item)
        except BotApiException as error:
            QMessageBox.warning(self, self._tr('Error'), str(error))
