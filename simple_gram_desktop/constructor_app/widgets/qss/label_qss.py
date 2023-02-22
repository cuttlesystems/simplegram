from enum import Enum
from typing import Optional
from dataclasses import dataclass

'''
Labels qss 
'''
"""-------------=========== qss for state flags bot ===========-------------"""


class ColorPalette(str, Enum):
    red = '#FF5F8F'
    blue = '#4DAAFF'


@dataclass(slots=True, frozen=True)
class LabelColorScheme:
    disabled = "QLabel{" \
               "border-radius:8px; border:none; " \
               "color:white;" \
               "background-color:"+ColorPalette.red+";}"

    enabled = "QLabel{" \
              "border-radius:8px; border:none; " \
              "color:white;" \
              "background-color:"+ColorPalette.blue+";}"
