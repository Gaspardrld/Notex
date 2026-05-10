from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel
from PySide6.QtGui import QColor
from styles.config import Color_System, Configuration
import json
import os
import sys
from startup import is_startup_enabled, enable_startup, disable_startup
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QColorDialog
from styles.config import*

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Color System:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems([c.name for c in Color_System])
        layout.addWidget(self.color_combo)
        
        layout.addWidget(QLabel("Configuration:"))
        self.config_combo = QComboBox()
        self.config_combo.addItems([c.name for c in Configuration])
        layout.addWidget(self.config_combo)
        

        layout.addWidget(QLabel("Add custom color theme"))
        save_btn = QPushButton("Pick colors")
        save_btn.clicked.connect(self.openColorPicker)
        layout.addWidget(save_btn)
        
        layout.addWidget(QLabel("Note: Changes will be applied after restarting the app."))
        save_btn = QPushButton("Save (restart to apply)")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        self.startup_checkbox = QCheckBox("Launch at Windows startup")
        self.startup_checkbox.setChecked(is_startup_enabled())
        layout.addWidget(self.startup_checkbox)
        
        self.setLayout(layout)
    
    def save(self):
        color = self.color_combo.currentText()
        config = self.config_combo.currentText()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "user_files", "user_config.json")

        with open(config_path, "w") as f:
            json.dump({"color_system": color, "configuration": config}, f, indent=2)
        
        if self.startup_checkbox.isChecked():
            enable_startup()
        else:
            disable_startup()
        
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def openColorPicker(self):        
        labels = ["Couleur texte", "Couleur fond", "Couleur accent"]
        colors = []

        for label in labels:
            color = QColorDialog.getColor(
                QColor("white"), self, f"Choisir — {label}"
            )
            if not color.isValid():
                return 
            colors.append(color)
        CONFIG_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "styles", "config.json"))
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        data["Color_System"]["CUSTOM"] = [
            colors[0].name(),
            colors[1].name(),
            colors[2].name()
        ]
        with open(CONFIG_PATH, "w") as f:
            json.dump(
                {
                    "Color_System": data["Color_System"],
                    "Configuration": {c.name: c.value for c in Configuration}
                },
                f,
                indent=2
            )
