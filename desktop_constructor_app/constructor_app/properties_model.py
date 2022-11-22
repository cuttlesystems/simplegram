import dataclasses
import typing

import PySide6
from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt


@dataclasses.dataclass
class PropertyInModel:
    name: str = ''
    value: str = ''


class PropertiesModel(QAbstractTableModel):
    _COLUMNS_COUNT = 2

    _COLUMN_PROPERTY_NAME = 0
    _COLUMN_PROPERTY_VALUE = 1

    _HEADER_COLUMNS = {
        0: 'Параметр',
        1: 'Значение'
    }

    def __init__(self, properties: typing.List[PropertyInModel]):
        super().__init__()
        self._properties: typing.List[PropertyInModel] = properties

    def rowCount(self, parent):
        return len(self._properties)

    def columnCount(self, parent):
        return self._COLUMNS_COUNT

    def data(self, index: QModelIndex, role: int):
        assert isinstance(index, QModelIndex)
        result = None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            column_number = index.column()
            row_number = index.row()
            property = self._properties[row_number]
            if column_number == self._COLUMN_PROPERTY_NAME:
                result = property.name
            elif column_number == self._COLUMN_PROPERTY_VALUE:
                result = property.value
        return result

    def setData(self, index: PySide6.QtCore.QModelIndex, value: typing.Any, role: int) -> bool:
        result = False
        if role == Qt.EditRole:
            if index.column() == self._COLUMN_PROPERTY_VALUE:
                parameter = self._properties[index.row()]
                parameter.value = value
                result = True
        return result

    def flags(self, index: PySide6.QtCore.QModelIndex) -> PySide6.QtCore.Qt.ItemFlag:
        result = super().flags(index)
        if index.column() == self._COLUMN_PROPERTY_VALUE:
            result |= Qt.ItemFlag.ItemIsEditable
        return result

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            result = None
        else:
            result = self._HEADER_COLUMNS.get(section)
        return result
