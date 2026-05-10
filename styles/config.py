from enum import Enum

class Color_System(Enum):
    DARK = ["white", "black", "black"]
    LIGHT = ["black", "white", "lightgray"]

class Configuration(Enum):
    CENTER_BAR = 1
    BOTTOM_RIGHT_BAR = 2