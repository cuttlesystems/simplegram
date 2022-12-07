import typing


def gen_next_name(base_name: str, used_names: typing.List[str]) -> str:
    test_name = base_name
    n = 2
    while test_name in used_names:
        test_name = f'{base_name} {n}'
        n += 1
    return test_name
