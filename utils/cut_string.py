def cut_string(string: str, max_chars: int) -> str:
    """
    Обрезает строку до указанного количества символов и добавляет ... в конец

    Args:
        string (str): Укорачиваемая строка
        max_chars (int): Максимальное количество символов

    Returns:
        str: Укороченная до max_chars символов строка + добавленные в конец ...
    """
    assert isinstance(string, str)
    assert isinstance(max_chars, int)

    if len(string) > max_chars:
        return string[:max_chars] + '...'
    return string
