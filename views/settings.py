from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QCheckBox, QColorDialog, QLineEdit, QHBoxLayout
from PySide6.QtGui import QColor, Qt
import json
import os
import sys
from startup import is_startup_enabled, enable_startup, disable_startup
from styles.config import*
from user_files.user_config import*

class SettingsWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Color System:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems([c.name for c in Color_System])
        self.color_combo.setCurrentText(color_system.name)
        layout.addWidget(self.color_combo)
        
        layout.addWidget(QLabel("Configuration:"))
        self.config_combo = QComboBox()
        self.config_combo.addItems([c.name for c in Configuration])
        self.config_combo.setCurrentText(configuration.name)
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

        layout.addWidget(QLabel("Clé API Mistral :"))

        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.Password)

        paste_btn = QPushButton("📋 Coller la clé API")
        paste_btn.clicked.connect(lambda: self.set_apikey(password_field.text()))

        toggle_btn = QPushButton("👁")
        toggle_btn.setFixedWidth(30)
        toggle_btn.clicked.connect(lambda: password_field.setEchoMode(
            QLineEdit.Normal if password_field.echoMode() == QLineEdit.Password else QLineEdit.Password
        ))

        api_row = QHBoxLayout()
        api_row.addWidget(paste_btn)
        api_row.addWidget(password_field)
        api_row.addWidget(toggle_btn)
        layout.addLayout(api_row)
        
        self.setLayout(layout)
    
    def set_apikey(self, key):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "user_files", "user_config.json")
        with open(config_path, "r+") as f:
            data = json.load(f)
            data["api_key"] = key
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def save(self):
        color = self.color_combo.currentText()
        config = self.config_combo.currentText()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "user_files", "user_config.json")

        try:
            with open(config_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data["color_system"] = color
        data["configuration"] = config

        with open(config_path, "w") as f:
            json.dump(data, f, indent=2)
        
        if self.startup_checkbox.isChecked():
            enable_startup()
        else:
            disable_startup()
        
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def openColorPicker(self):
        labels = ["Couleur texte", "Couleur fond", "Couleur bord"]
        colors = []
        screen = QApplication.primaryScreen().availableGeometry()

        for label in labels:
            dialog = QColorDialog(QColor("white"), self)
            dialog.setWindowTitle(f"Choisir — {label}")
            dialog.adjustSize()
            dialog.move(
                (screen.width() - dialog.width()) // 2,
                (screen.height() - dialog.height()) // 2
            )
            if not dialog.exec():
                return
            colors.append(dialog.selectedColor())
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

    def open_settings(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setStyleSheet("background: "+color_system.value[2]+"; color:"+color_system.value[0]+";")
        screen = QApplication.primaryScreen().availableGeometry()
        self.adjustSize()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        self.show()
