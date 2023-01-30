import typing

from PySide6.QtWidgets import QWidget

from constructor_app.widgets.ui_client_widget import Ui_ClientWidget

class ClientWidget(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self._ui = Ui_ClientWidget()
        self._ui.setupUi(self)
        self._start_LoginUsers()

    def _start_LoginUsers(self) ->None:
        self._ui.centralPannelWidget.setCurrentIndex(0)
        self._ui.SideBar.hide()
        self._ui.topPannel.hide()

    def _start_MainMenu(self) ->None:
        self._ui.centralPannelWidget.setCurrentIndex(1)
        self._ui.SideBar.show()
        self._ui.topPannel.show()