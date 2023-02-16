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

class SettingsWidget(QWidget):
    """
    Надстройка выводимого пользователю GUI
    """

    def __init__(self, parent: Optional[QWidget] = None):
        # toDO: Добавить функцию инициализации QSS
        super().__init__(parent)

        self._ui = Ui_SettingsWidget()
        self._ui.setupUi(self)
        self._ui.apply_button.clicked.connect(self._on_apply_clicked)
        self._ui.cancel_button.clicked.connect(self._on_cancel_clicked)

        self._ui.language_combo.clear()
        self._ui.language_combo.addItem('English language', LanguagesEnum.ENGLISH)
        self._ui.language_combo.addItem('Русский язык', LanguagesEnum.RUSSIAN)
        self._ui.language_combo.addItem('Қазақ тілі', LanguagesEnum.KAZAKH)

        self._language_settings_manager = LanguageSettingsManager()

        selected_language = self._language_settings_manager.read_settings().language
        for index in range(self._ui.language_combo.count()):
            data = self._ui.language_combo.itemData(index)
            if data == selected_language:
                self._ui.language_combo.setCurrentIndex(index)

        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    def _on_apply_clicked(self) -> None:
        index = self._ui.language_combo.currentIndex()
        data = self._ui.language_combo.itemData(index)
        self._language_settings_manager.write_settings(LanguageSettings(language=data))
        QtWidgets.QMessageBox.information(self, self._tr('Info message'),
                                          self._tr('The changes you made will take '
                                                   'effect after the application is restarted.'))
        self.close()

    def _on_cancel_clicked(self) -> None:
        self.close()

    def _tr(self, text: str) -> str:
        return tran('SettingsWidget.manual', text)

