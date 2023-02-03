import typing
from PySide6.QtWidgets import QWidget,QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import SIGNAL, SLOT


from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from common.localisation import tran

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget
from constructor_app.widgets.bot_editor.bot_editor_form import BotEditorForm

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

    def __init__(self, parent: typing.Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)

        # дружу кнопку ентера при авторизации и инициализации мейн окна
        self._ui.loginWindow.log_in.connect(self._start_main_menu)
        # дружу
        self._ui.botNewCreator.close_window.connect(self._start_main_menu)

        """Сайдбар"""
        # дружу кнопку нового проекта и инициализацию окна создания бота
        self._ui.new_project_button.clicked.connect(self._start_new_project)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.bot_list.clicked.connect(self._start_selected_project)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.logo_block.clicked.connect(self._start_main_menu)
        # дружу нажатие по сайдбару и инициализацию окна с шапкой выбранного бота
        self._ui.botShowWindow.open_bot_in_redactor_signal.connect(self._start_bot_redactor)

        # первое открытие приложения, инициализация авторизации
        self._start_login_users()

    # инициализация окна авторизации
    def _start_login_users(self) -> None:
        # выстравляю страницу инициализации
        self._ui.centrall_pannel_widget.setCurrentIndex(self._LOGIN_INDEX_PAGE)
        # прячу сайдбар и топпанел
        self._ui.side_bar.hide()
        self._ui.top_pannel.hide()


    # инициализация основого окна приложения
    def _start_main_menu(self) -> None:
        # выстравляю страницу главного окна
        self._ui.centrall_pannel_widget.setCurrentIndex(self._MAIN_MENU_INDEX_PAGE)
        self._init_stylesheet_stackedwidget(0)
        # показываю сайдбар и топпанел
        self._ui.side_bar.show()
        self._ui.top_pannel.show()
        self._ui.tool_stack.hide()
        self._init_projectslist()

    # инициализация окна с информацией о выбранном боте
    def _start_selected_project(self) -> None:
        # выстравляю страницу с информацией о выбранном боте
        self._ui.centrall_pannel_widget.setCurrentIndex(self._SELECTED_BOT_INDEX_PAGE)
        self._ui.tool_stack.hide()
        self._init_stylesheet_stackedwidget(0)

    def _start_new_project(self) -> None:
        # инициализация окна с добавлением нового бота
        # выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._NEW_BOT_INDEX_PAGE)
        self._ui.tool_stack.hide()
        # настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(1)

    def _start_bot_redactor(self) -> None:
        # выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(self._BOT_REDACTOR_PAGE)
        self._ui.tool_stack.show()
        # настраиваю таблицу стилей подложки
        self._init_stylesheet_stackedwidget(0)
        # связь окон редактироавания и панели инструментария
        self.__bot_editor_connector()

    def __bot_editor_connector(self):
        # toDo: Засунуть в BotRedactorWindow метод с setToolStack
        # toDo: Переименовать страницы в StackWidget под общую стилистику
        self._ui.botRedactorWindow.delete_variant_setEnabled.connect(self._ui.tool_stack.delete_variant_setState)
        self._ui.botRedactorWindow.delete_message_setEnabled.connect(self._ui.tool_stack.delete_message_setState)
        self._ui.botRedactorWindow.mark_error_setEnabled.connect(self._ui.tool_stack.mark_error_setState)
        self._ui.botRedactorWindow.mark_start_setEnabled.connect(self._ui.tool_stack.mark_start_setState)
        self._ui.botRedactorWindow.add_variant_setEnabled.connect(self._ui.tool_stack.add_variant_setState)

        self._ui.tool_stack.delete_variant_signal.connect(self._ui.botRedactorWindow.on_delete_variant)
        self._ui.tool_stack.mark_as_start_signal.connect(self._ui.botRedactorWindow.on_mark_as_start_button)
        self._ui.tool_stack.add_variant_signal.connect(self._ui.botRedactorWindow.on_action_add_variant)
        self._ui.tool_stack.mark_as_error_signal.connect(self._ui.botRedactorWindow.on_mark_as_error_button)
        self._ui.tool_stack.add_message_signal.connect(self._ui.botRedactorWindow.on_add_new_message)
        self._ui.tool_stack.generate_bot_signal.connect(self._ui.botRedactorWindow.on_generate_bot)
        self._ui.tool_stack.start_bot_signal.connect(self._ui.botRedactorWindow.on_start_bot)
        self._ui.tool_stack.stop_bot_signal.connect(self._ui.botRedactorWindow.on_stop_bot)
        self._ui.tool_stack.read_bot_logs_signal.connect(self._ui.botRedactorWindow.on_read_bot_logs)
        self._ui.tool_stack.delete_message_signal.connect(self._ui.botRedactorWindow.on_delete_message)

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
        # toDo: Добавить подгрузку списка проектов с сервера
        self._ui.bot_list.add_bot(QPixmap(":/icons/widgets/times_icon/newProject.png"), "BotNew", False, 0)

    def _tr(self, text: str) -> str:
        return tran('ClientWidget.manual', text)