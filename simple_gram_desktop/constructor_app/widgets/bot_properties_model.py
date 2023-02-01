from common.localisation import tran
from common.model_property import ModelProperty
from common.properties_model import PropertiesModel


class BotPropertiesModel(PropertiesModel):
    """
    Модель свойств бота
    """

    def __init__(self):
        self._prop_name = ModelProperty(name=self._tr('Bot name'))
        self._prop_token = ModelProperty(name=self._tr('Bot token'))
        self._prop_description = ModelProperty(name=self._tr('Description'))
        self._prop_link = ModelProperty(name=self._tr('Link to bot'))

        super().__init__([
            self._prop_name,
            self._prop_token,
            self._prop_description,
            self._prop_link
        ])

    def get_name(self) -> str:
        return self._prop_name.value

    def set_name(self, value: str):
        self.beginResetModel()
        try:
            self._prop_name.value = value
        finally:
            self.endResetModel()

    def get_token(self) -> str:
        return self._prop_token.value

    def set_token(self, value: str):
        self.beginResetModel()
        try:
            self._prop_token.value = value
        finally:
            self.endResetModel()

    def get_description(self) -> str:
        return self._prop_description.value

    def set_description(self, value: str):
        self.beginResetModel()
        try:
            self._prop_description.value = value
        finally:
            self.endResetModel()

    def get_link(self) -> str:
        return self._prop_link.value

    def set_link(self, value: str):
        self.beginResetModel()
        try:
            self._prop_link.value = value
        finally:
            self.endResetModel()

    def _tr(self, mes: str) -> str:
        return tran('BotPropertiesModel.manual', mes)
