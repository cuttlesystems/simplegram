from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BlockColorScheme:
    message_color = 0xceffff
    text_color = 0x154545
    pen_color = 0x137b7b

    variant_background = 0x9edee6
    selected_variant_background = 0x84d2dc
