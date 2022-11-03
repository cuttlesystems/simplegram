import typing

def create_keyboard_array(id: int, variants: typing.List[dict]) -> typing.List[str]:
    return [item['text'] for item in variants if item['current_id']==id]