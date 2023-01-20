from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BlockColorScheme:
    """
    Цветовая схема блока
    """

    # цвет фона сообщения
    message_color = 0xceffff

    # цвет первого сообщения
    start_message_color = 0xe49ae6

    # цвет ошибочного сообщения
    error_message_color = 0xed645a

    # цвет, если сообщение и стартовое, и ошибочное
    start_and_error_message_color = 0xedc360

    # цвет текста
    text_color = 0x154545

    # цвет контура сообщения и варианта
    pen_color = 0x137b7b

    # фон варианта (когда не выделен)
    variant_background = 0x9edee6

    # фон варианта (когда выделен)
    selected_variant_background = 0x84d2dc
