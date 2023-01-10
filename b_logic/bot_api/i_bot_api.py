from typing import List
from abc import abstractmethod, ABC

from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypes, BotCommand, BotLogs


class BotApiException(Exception):
    def __init__(self, mes: str):
        super().__init__(mes)


class IBotApi(ABC):
    @abstractmethod
    def set_suite(self, suite_url: str) -> None:
        """
        Устанавливает suite_url: корневой URL для API запросов
        Args:
            suite_url: URL запроса
        """
        pass

    @abstractmethod
    def sign_up(self, username: str, email: str, password: str) -> None:
        """
        Регистрация нового пользователя.

        Args:
            username: Имя
            email: Электронная почта
            password: Пароль
        """
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
    def get_bots(self) -> List[BotDescription]:
        """
        Получить список ботов пользователя
        Returns:
            список ботов
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
            bot: описание бота
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
    def create_message(self, bot: BotDescription, text: str,
                       keyboard_type: ButtonTypes, x: int, y: int) -> BotMessage:
        """
        Создать сообщение
        Args:
            bot: объект бота, для которого создается сообщение
            text: тест сообщения
            keyboard_type: тип клавиатуры (inline or reply)
            x: координата по x
            y: координата по y

        Returns:
            объект созданного сообщения
        """
        pass

    @abstractmethod
    def change_message(self, message: BotMessage) -> None:
        """
        Изменить сообщение
        Args:
            message: сообщение, которое необходимо изменить
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

    @abstractmethod
    def get_variants(self, message: BotMessage) -> List[BotVariant]:
        """
        Получить варианты для заданного сообщения
        Args:
            message: сообщение для которого получаем варианты

        Returns:
            список вариантов
        """
        pass

    @abstractmethod
    def create_variant(self, message: BotMessage, text: str) -> BotVariant:
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
    def change_variant(self, variant: BotVariant) -> None:
        """
        Изменение варианта

        Args:
            variant: вариант который необходимо изменить
        """
        pass

    @abstractmethod
    def connect_variant(self, variant: BotVariant,
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
    def delete_variant(self, variant: BotVariant) -> None:
        """
        Удаление варианта

        Args:
            variant: вариант который необходимо удалить
        """
        pass

    @abstractmethod
    def get_commands(self, bot: BotDescription) -> List[BotCommand]:
        """
        Получить команды для заданного бота

        Args:
            bot: бот для которого получаем команды

        Returns:
            список команд
        """
        pass

    @abstractmethod
    def create_command(self, bot: BotDescription, command: str, description: str) -> BotCommand:
        """
        Создание команды.

        Args:
            bot: бот для которого получаем команды
            command: имя команды
            description: краткое описание команды

        Returns:
            Объект BotCommand
        """
        pass

    @abstractmethod
    def generate_bot(self, bot: BotDescription) -> None:
        """
        Сгенерировать код бота.

        Args:
            bot (BotDescription): Бот которого необходимо сгенерировать.
        """
        pass

    @abstractmethod
    def start_bot(self, bot: BotDescription) -> None:
        """
        Запуск сгенерированного бота.

        Args:
            bot (BotDescription): Бот которого необходимо запустить.
        """
        pass

    @abstractmethod
    def stop_bot(self, bot: BotDescription) -> None:
        """
        Остановка запущенного бота.

        Args:
            bot (BotDescription): Бот которого необходимо остановить.
        """
        pass

    @abstractmethod
    def get_running_bots_info(self) -> List[int]:
        """
        Получает данные о запущенных ботах пользователя.

        Returns: Список id запущенных ботов.
        """
        pass

    @abstractmethod
    def get_bot_logs(self, bot: BotDescription) -> BotLogs:
        """
        Получить логи бота (stdout, stderr)
        Args:
            bot: бот у которого получаем логи

        Returns:
            объект с логами бота
        """
        pass
