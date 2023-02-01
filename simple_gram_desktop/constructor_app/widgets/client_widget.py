import typing
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import SIGNAL, SLOT

from common.localisation import tran

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget

class ClientWidget(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        print('create ClientWidget')

        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)

        #дружу кнопку ентера при авторизации и инициализации мейн окна
        self._ui.loginWindow.log_in.connect(self._start_main_menu)
        #дружу
        self._ui.botNewCreator.close_window.connect(self._start_main_menu)

        """Сайдбар"""
        #дружу кнопку нового проекта и инициализации окна создания бота
        self._ui.new_project_button.clicked.connect(self._start_new_roject)
        self._ui.projects_list.clicked.connect(self._start_selected_project)
        self._ui.logo_block.clicked.connect(self._start_main_menu)

        #первое открытие приложения, инициализация авторизации
        self._start_login_users()

    #инициализация окна авторизации
    def _start_login_users(self) ->None:
        #выстравляю страницу инициализации
        self._ui.centrall_pannel_widget.setCurrentIndex(0)
        # прячу сайдбар и топпанел
        self._ui.side_bar.hide()
        self._ui.top_pannel.hide()

    #инициализация основого окна приложения
    def _start_main_menu(self) ->None:
        #выстравляю страницу главного окна
        self._ui.centrall_pannel_widget.setCurrentIndex(1)
        self._init_stylesheet_stackedwidget(0)
        #показываю сайдбар и топпанел
        self._ui.side_bar.show()
        self._ui.top_pannel.show()

    # инициализация основого окна приложения
    def _start_selected_project(self) ->None:
        #выстравляю страницу с информацией о выбранном боте
        self._ui.centrall_pannel_widget.setCurrentIndex(2)
        self._init_stylesheet_stackedwidget(0)

    # инициализация основого окна приложения
    def _start_new_roject(self) ->None:
        #выстравляю страницу добавления новго бота
        self._ui.centrall_pannel_widget.setCurrentIndex(3)
        self._init_stylesheet_stackedwidget(1)

#toDO: перенести все qssы в отдельный файлпроекта или для каждого окна сделать свой первострочный инициализатор qss
    def _init_stylesheet_stackedwidget(self, state:int) -> None:
        if (state == 0):
            self._ui.centrall_pannel_widget.setStyleSheet("QStackedWidget{border: none;background: rgb(241,241,241);}")
        else:
            self._ui.centrall_pannel_widget.setStyleSheet("QStackedWidget{border: none;background: rgb(105,105,109);}")

    def _tr(self, text: str) -> str:
        return tran('ClientGUI.manual', text)