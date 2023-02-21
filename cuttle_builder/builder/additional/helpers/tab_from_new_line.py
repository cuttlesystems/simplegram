
def tab_from_new_line(code: str) -> str:
    """
    Prepare generate code: replace next string to new line and add tabulation
    Args:
        code (str): code, that will writen in file
    Returns:
        prepared string, that move next string to new line and add tabulation
    """
    assert isinstance(code, str)
    return f'{code}\n\t'
