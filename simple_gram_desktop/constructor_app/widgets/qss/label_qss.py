from enum import Enum
from typing import Optional
from dataclasses import dataclass

'''
Labels qss 
'''
"""-------------=========== qss for state flags bot ===========-------------"""


class ColorPalette(str, Enum):
    RED = '#FF5F8F'
    BLUE = '#4DAAFF'


@dataclass(slots=True, frozen=True)
class LabelColorScheme:
    DISABLED = "QLabel{" \
               "border-radius:8px; border:none; " \
               "color:white;" \
               "background-color:"+ColorPalette.RED+";}"

    ENABLED = "QLabel{" \
              "border-radius:8px; border:none; " \
              "color:white;" \
              "background-color:"+ColorPalette.BLUE+";}"
