from typing import List, Optional
from dataclasses import dataclass

from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from PySide6.QtCore import Qt, Signal
from PySide6 import QtWidgets, QtGui, QtCore
from common.localisation import tran

from constructor_app.widgets.ui_settings_widget import Ui_SettingsWidget
from constructor_app.settings.language_settings_manager import LanguageSettingsManager
from constructor_app.settings.languages_enum import LanguagesEnum
from constructor_app.settings.language_settings import LanguageSettings


@dataclass(slots=True)
class ComboItem:
    # toDo: Renaming BotExtended
    combo_item: str
    language_item: LanguagesEnum


class SettingsWidget(QWidget):
    """
    Надстройка выводимого пользователю GUI
    """
    restart_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_SettingsWidget()
        self._ui.setupUi(self)
        self._ui.apply_button.clicked.connect(self._on_apply_clicked)
        self._ui.cancel_button.clicked.connect(self._on_cancel_clicked)

        self._combo_list: List[ComboItem] = list()
        self._combo_list.append(
            ComboItem(
                combo_item=self._ui.language_combo.itemData(0, QtCore.Qt.ItemDataRole.DisplayRole),
                language_item=LanguagesEnum.ENGLISH))
        self._combo_list.append(
            ComboItem(
                combo_item=self._ui.language_combo.itemData(1, QtCore.Qt.ItemDataRole.DisplayRole),
                language_item=LanguagesEnum.RUSSIAN))
        self._combo_list.append(
            ComboItem(
                combo_item=self._ui.language_combo.itemData(2, QtCore.Qt.ItemDataRole.DisplayRole),
                language_item=LanguagesEnum.KAZAKH))

        self._language_settings_manager = LanguageSettingsManager()

        #toDo: добавить инициализацию языка
        self._ui.language_combo.setCurrentIndex(0)

        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    def _on_apply_clicked(self) -> None:
        index = self._ui.language_combo.currentIndex()
        language_setting = self._combo_list.__getitem__(index)
        self._language_settings_manager.write_settings(LanguageSettings(language=language_setting.language_item))
        QtWidgets.QMessageBox.information(self, self._tr('Info message'),
                                          self._tr('The changes you made will take '
                                                   'effect after the application is restarted.'))
        self.close()

    def _on_cancel_clicked(self) -> None:
        self.close()

    def _tr(self, text: str) -> str:
        return tran('SettingsWidget.manual', text)

