from typing import Optional

from PySide6.QtGui import QPixmap, QImage


def get_pixmap_image_from_bytes(image_data: Optional[bytes]) -> Optional[QPixmap]:
    """
    Создает объект QPixmap из байт-кода изображения.
    Args:
        image_data: Изображение в формате байт-кода.
    Returns:
        Изображение в виде объекта QPixmap.
    """
    assert isinstance(image_data, Optional[bytes])
    result = None
    if image_data is not None:
        image = QImage()
        image.loadFromData(image_data)
        result = QPixmap(image)
    return result
