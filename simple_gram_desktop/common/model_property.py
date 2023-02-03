import dataclasses


@dataclasses.dataclass(slots=True)
class ModelProperty:
    name: str = ''
    value: str = ''
