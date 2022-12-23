from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BlockColorScheme:
    """
    Цветовая схема блока
    """

    # цвет фона сообщения
    message_color = 0xceffff

    # цвет текста
    text_color = 0x154545

    # цвет контура сообщения и варианта
    pen_color = 0x137b7b

    # фон варианта (когда не выделен)
    variant_background = 0x9edee6

    # фон варианта (когда выделен)
    selected_variant_background = 0x84d2dc
