from PySide6.QtCore import QCoreApplication


def tran(context: str, text: str) -> str:
    """
    Функция для локализации (перевода) текста
    Args:
        context: контекст перевода
        text: сообщения для перевода (на английском)

    Returns:
        локализованное сообщение
    """
    assert isinstance(context, str)
    assert isinstance(text, str)
    return QCoreApplication.translate(context, text)
