import typing

import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt

from desktop_constructor_app.common.model_property import ModelProperty


class PropertiesModel(QAbstractTableModel):
    _COLUMNS_COUNT = 2

    _COLUMN_PROPERTY_NAME = 0
    _COLUMN_PROPERTY_VALUE = 1

    _HEADER_COLUMNS: typing.Dict[int, str] = {
        0: 'Параметр',
        1: 'Значение'
    }

    def __init__(self, properties: typing.List[ModelProperty]):
        super().__init__()
        self._properties: typing.List[ModelProperty] = properties

    def rowCount(self, parent: QModelIndex):
        assert isinstance(parent, QModelIndex)
        return len(self._properties)

    def columnCount(self, parent: QModelIndex):
        assert isinstance(parent, QModelIndex)
        return self._COLUMNS_COUNT

    def data(self, index: QModelIndex, role: int):
        assert isinstance(index, QModelIndex)
        assert isinstance(role, int)
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

    def setData(self, index: QModelIndex, value: typing.Any, role: int) -> bool:
        assert isinstance(index, QModelIndex)
        assert isinstance(role, int)
        result = False
        if role == Qt.ItemDataRole.EditRole:
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

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> typing.Optional[str]:
        assert isinstance(section, int)
        assert isinstance(orientation, Qt.Orientation)
        assert isinstance(role, int)
        result = None
        if role == Qt.DisplayRole and orientation == Qt.Orientation.Horizontal:
            result = self._HEADER_COLUMNS.get(section)
        return result
