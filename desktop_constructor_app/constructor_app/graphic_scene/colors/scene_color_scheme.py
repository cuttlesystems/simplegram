from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SceneColorScheme:
    # цвет фона рабочей области
    workspace_background_color = 0xf0ffff

    # цвет линии границы рабочей области
    workspace_background_border_color = 0xc5ecec
