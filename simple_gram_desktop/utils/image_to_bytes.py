from typing import Optional


def get_binary_data_from_image_file(path_to_file: str) -> Optional[bytes]:
    """
    Конвертация файла по path в байт-код.

    Args:
        path_to_file: путь к файлу.

    Returns:
        байт-код изображения.
    """
    assert isinstance(path_to_file, str)
    image_data = None
    try:
        with open(path_to_file, 'rb') as file:
            image_data = file.read()
    except FileNotFoundError as error:
        print(f'CHANGE_TO_LOGGING-------> File not found error: {error}')
    return image_data
