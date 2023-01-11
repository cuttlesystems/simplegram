import inspect
import logging.handlers
from .settings import PROJECT_ROOT_DIR_NAME

# Настройки логеров определены в settings.py в переменной LOGGING (dict) по ключу 'loggers'
_LOGGER_DJANGO = logging.getLogger('django')


class BackendLogger:
    """
    Класс-оболочка для логирования внутри проекта.
    """
    def __init__(self, logger: logging.Logger):
        assert isinstance(logger, logging.Logger)
        self.logger = logger

    def debug_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.debug(f'{path_to_file} - {message}')

    def info_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.info(f'{path_to_file} - {message}')

    def warning_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.warning(f'{path_to_file} - {message}')

    def error_logging(self, message: str) -> None:
        assert isinstance(message, str)
        path_to_file = self._remove_home_dirs_from_path(self._get_path_from_call_stack())
        self.logger.error(f'{path_to_file} - {message}')

    def _get_path_from_call_stack(self) -> str:
        """
        Возвращает путь к файлу в котором был вызван логгер.

        Returns: Полный путь к файлу
        """
        return inspect.stack()[2].filename

    def _remove_home_dirs_from_path(self, path: str) -> str:
        """
        Возвращает путь начиная с корневой директории проекта.

        Args:
            path: Полный путь к файлу

        Returns: Путь к файлу начиная с корневой директории.
        """
        assert isinstance(path, str)
        path_list = path.split('/')
        try:
            index = path_list.index(PROJECT_ROOT_DIR_NAME)
        except ValueError:
            index = 0
        return '/'.join(path_list[index:])


logger_django = BackendLogger(_LOGGER_DJANGO)
