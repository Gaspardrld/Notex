import json
import os
from styles.config import Color_System, Configuration

_config_path = os.path.join(os.path.dirname(__file__), "user_config.json")

def _load():
    try:
        with open(_config_path) as f:
            data = json.load(f)
        return Color_System[data["color_system"]], Configuration[data["configuration"]]
    except (FileNotFoundError, KeyError):
        return Color_System.DARK, Configuration.CENTER_BAR

color_system, configuration = _load()
