from PySide6.QtCore import QCoreApplication


def tran(context: str, text: str) -> str:
    assert isinstance(context, str)
    assert isinstance(text, str)
    return QCoreApplication.translate(context, text)
