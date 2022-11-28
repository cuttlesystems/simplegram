from desktop_constructor_app.common.model_property import ModelProperty
from desktop_constructor_app.common.properties_model import PropertiesModel


class BotPropertiesModel(PropertiesModel):
    def __init__(self):
        self._prop_name = ModelProperty(name='Название бота', value='')
        self._prop_token = ModelProperty(name='Токен бота', value='')
        self._prop_description = ModelProperty(name='Описание', value='')

        super().__init__([
            self._prop_name,
            self._prop_token,
            self._prop_description
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
