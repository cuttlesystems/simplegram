import typing

from b_logic.data_objects import BotMessage, BotVariant


def find_previous_messages(message_id: int, messages: typing.List[BotMessage]) -> typing.List[BotMessage]:
    """Получает список собщении у которых next_message == message.id (принемаемый
    на вход функцией)

    Args:
        message_id (int): id of current message
        messages:

    Returns:
        typing.List[dict]: list of all previous messages for concrete message
    """
    return [item for item in messages if item.next_message_id == message_id]


def find_previous_variants(message_id: int, variants: typing.List[BotVariant]) -> typing.List[BotVariant]:
    """Получает список вариантов у которых next_message == message.id (принемаемый
    на вход функцией)

    Args:
        variants:
        message_id (int): id of current message

    Returns:
        typing.List[dict]: list of all previous variants for concrete message
    """
    return [item for item in variants if item.next_message_id == message_id]


def find_variants_of_message(message_id: int, variants: typing.List[BotVariant]) -> typing.List[BotVariant]:
    """generate list of variants, names of buttons in keyboard

    Args:
        variants:
        message_id (int): id of message

    Returns:
        typing.List[MessageVariant]: list of variants (keyboard buttons) related to concrete message
    """
    return [item for item in variants if item.current_message_id == message_id]
