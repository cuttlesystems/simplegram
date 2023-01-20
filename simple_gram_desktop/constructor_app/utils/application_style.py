from PySide6.QtWidgets import QStyleFactory


def print_available_styles() -> None:
    styles = ', '.join(QStyleFactory.keys())
    print('Available application styles (-style): {styles}.'.format(styles=styles))
    # еще можно так под windows:
    # sys.argv += ['-platform', 'windows:darkmode=2']
