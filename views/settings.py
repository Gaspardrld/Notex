from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel
from styles.config import Color_System, Configuration
import os
import sys
from startup import is_startup_enabled, enable_startup, disable_startup
from PySide6.QtWidgets import QCheckBox

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
        config_path = os.path.join(base_dir, "user_files", "user_config.py")
        
        with open(config_path, "w") as f:
            f.write("from styles.config import *\n\n")
            f.write(f"color_system = Color_System.{color}\n")
            f.write(f"configuration = Configuration.{config}\n")
        
        if self.startup_checkbox.isChecked():
            enable_startup()
        else:
            disable_startup()
        
        os.execv(sys.executable, [sys.executable] + sys.argv)

