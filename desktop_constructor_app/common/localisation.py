from PySide6.QtCore import QCoreApplication


def tran(context: str, text: str) -> str:
    assert isinstance(context, str)
    assert isinstance(text, str)
    context_bytes = context.encode('utf-8')
    text_bytes = text.encode('utf-8')
    return QCoreApplication.translate(context_bytes, text_bytes)
