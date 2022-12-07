import typing


def gen_next_name(base_name: str, used_names: typing.List[str]) -> str:
    """
    Сгенерировать уникальное имя по базовому имени.
    Уникальное имя получается из базового имени путем добавления числа
    Args:
        base_name: Базовое имя
        used_names: Список уже занятых имен

    Returns: Уникальное (незанятое) имя
    """
    test_name = base_name
    n = 2
    while test_name in used_names:
        test_name = f'{base_name} {n}'
        n += 1
    return test_name
