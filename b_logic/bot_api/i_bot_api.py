from typing import List
from abc import abstractmethod, ABC

from b_logic.data_objects import BotDescription, BotMessage, MessageVariant


class BotApiException(Exception):
    def __init__(self, mes: str):
        super().__init__(mes)


class IBotApi(ABC):
    @abstractmethod
    def set_suite(self, suite_url: str) -> None:
        """Устанавливает suite_url: корневой URL для API запросов"""
        pass

    @abstractmethod
    def authentication(self, username: str, password: str) -> None:
        """
        Провести аутентификацию пользователя и запомнить токен авторизации для
        дальнейшего вызова методов
        Args:
            username: имя пользователя
            password: пароль
        """
        pass

    @abstractmethod
    def auth_by_token(self, token: str) -> None:
        """
        Авторизация пользователя по токену
        Args:
            token: токен авторизации
        """
        pass

    @abstractmethod
    def create_bot(self, bot_name: str,
                   bot_token: str, bot_description: str) -> BotDescription:
        """
        Создать бота
        Args:
            bot_name: название бота
            bot_token: токен бота
            bot_description: описание бота

        Returns:
            объект созданного бота
        """
        pass

    @abstractmethod
    def get_bots(self) -> List[BotDescription]:
        """
        Получить список ботов пользователя
        Returns:
            список ботов
        """
        pass

    @abstractmethod
    def get_bot_by_id(self, id: int) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        Args:
            id: идентификатор бота

        Returns:
            объект бота
        """
        pass

    @abstractmethod
    def change_bot(self, bot: BotDescription) -> None:
        """
        Изменить бота
        Args:
            bot_name: название бота
            bot_token: токен бота
            bot_description: описание бота
        """
        pass

    @abstractmethod
    def delete_bot(self, id: int) -> None:
        """
        Удалить бота
        Args:
            id: идентификатор бота
        """
        pass

    @abstractmethod
    def create_message(self, bot: BotDescription,
                       text: str, x: int, y: int) -> BotMessage:
        """
        Создать сообщение
        Args:
            bot: объект бота, для которого создается сообщение
            text: тест сообщения
            x: координата по x
            y: координата по y

        Returns:
            объект созданного сообщения
        """
        pass

    @abstractmethod
    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        """
        Получить все сообщения заданного бота
        Args:
            bot: бот, у которого нужно получить сообщения

        Returns:
            список сообщений бота
        """
        pass

    @abstractmethod
    def create_variant(self, message: BotMessage, text: str) -> MessageVariant:
        """
        Создание варианта
        Args:
            message: объект сообщения для которого создается вариант
            text: текст создаваемого варианта

        Returns:
            объект созданного варианта
        """
        pass

    @abstractmethod
    def get_variants(self, message: BotMessage) -> List[MessageVariant]:
        """
        Получить варианты для заданного сообщения
        Args:
            message: сообщение для которого получаем варианты

        Returns:
            список вариантов
        """
        pass

    @abstractmethod
    def connect_variant(self, variant: MessageVariant,
                        message: BotMessage) -> None:
        """
        Связать вариант и сообщение, к которому перейдем при выборе
        этого варианта
        Args:
            variant: связываемый вариант
            message: сообщение к которому перейдем
        """
        pass

    @abstractmethod
    def set_bot_start_message(self, bot: BotDescription,
                              start_message: BotMessage) -> None:
        """
        Установить сообщение с которого начнется работа с ботом
        Args:
            bot: объект бота
            start_message: объект сообщения, которое будет установлено в
            качестве стартового
        """
        pass

    @abstractmethod
    def delete_message(self, message: BotMessage) -> None:
        """
        Удалить сообщение из бота
        Args:
            message: сообщение, которое требуется удалить
        """
        pass

    def change_message(self, message: BotMessage) -> None:
        """
        Изменить сообщение
        Args:
            message: сообщение, которое необходимо изменить
        """
        pass
