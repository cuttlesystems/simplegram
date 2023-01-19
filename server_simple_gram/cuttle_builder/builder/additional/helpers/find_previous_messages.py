import typing

def find_previous_messages(id: int, variants: typing.List[dict]) -> typing.List[dict]:
    return [item for item in variants if item['next_id']==id]
    