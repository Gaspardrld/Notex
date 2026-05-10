from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QSystemTrayIcon, QMenu, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction
import os
import sys
from datetime import datetime
from user_files.user_config import*
from views.settings import SettingsWindow
from PySide6.QtGui import QShortcut, QKeySequence


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: "+color_system.value[2]+";")

        if configuration == Configuration.CENTER_BAR:
            screen = QApplication.primaryScreen().availableGeometry()
            w, h = 600, 60
            self.setGeometry((screen.width() - w) // 2, ((screen.height() - h) // 2)-70, w, h)

        if configuration == Configuration.BOTTOM_RIGHT_BAR:
            screen = QApplication.primaryScreen().availableGeometry()
            w, h = 400, 150
            self.setGeometry(screen.width() - w - 10, screen.height() - h - 10, w, h)

        shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        shortcut.activated.connect(open_settings)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        if event.key() == Qt.Key_Q and event.modifiers() & Qt.ControlModifier:
            self.close()
        if event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            open_settings()

class NoteLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Tell Punch what's on your mind...")
        self.setStyleSheet("font-size: 16px; padding: 10px; color:"+color_system.value[0]+"; background:"+color_system.value[1]+"; border: none; outline: none;")
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setGeometry(10, 10, self.parent().width()-20, self.parent().height()-20)
        notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_files")
        os.makedirs(notes_dir, exist_ok=True)
        self._notes_path = os.path.join(notes_dir, "note.txt")
        # pre-warm file I/O so the first save isn't slow
        with open(self._notes_path, "a", encoding="utf-8"):
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.write_text()
            self.clear()
            self.setReadOnly(True)
            self.setText("✓")
            QTimer.singleShot(500, lambda: self.setText(""))
            QTimer.singleShot(500, lambda: self.setReadOnly(False))
        else:
            super().keyPressEvent(event)

    def write_text(self):
        with open(self._notes_path, "a", encoding="utf-8") as file:
            file.write(datetime.now().strftime("%d/%m/%Y %H:%M"))
            file.write("\n")
            file.write(self.text())
            file.write("\n\n")


f = open("monapp.lock", "w")
try:
    import msvcrt
    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
except OSError:
    sys.exit(0)
app = QApplication([])
settings_window = SettingsWindow()

def open_settings():
    settings_window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    settings_window.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
    settings_window.setStyleSheet("background: "+color_system.value[2]+"; color:"+color_system.value[0]+";")
    screen = QApplication.primaryScreen().availableGeometry()
    settings_window.adjustSize()
    settings_window.move(
        (screen.width() - settings_window.width()) // 2,
        (screen.height() - settings_window.height()) // 2
    )
    settings_window.show()


icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "icon.png")
icon = QIcon(icon_path)
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

app.setQuitOnLastWindowClosed(False)
window = MainWindow()


note_input = NoteLineEdit(window)