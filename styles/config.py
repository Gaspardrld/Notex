import json
import os
from enum import Enum

_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(_path) as f:
    _data = json.load(f)

Color_System = Enum("Color_System", {k: v for k, v in _data["Color_System"].items()})
Configuration = Enum("Configuration", {k: v for k, v in _data["Configuration"].items()})
