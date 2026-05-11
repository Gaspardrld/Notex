from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QSystemTrayIcon, QMenu, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction
import os
import sys
from datetime import datetime

from user_files.user_config import*
from views.settings import SettingsWindow
from PySide6.QtGui import QShortcut, QKeySequence
from enum import*
from mistral_.mistral_retriever import ask_mistral


MAX_HEIGHT = 400
class States(Enum):
    EDIT_RUNNING = 1 
    AI_RUNNING = 2

class MainWindow(QMainWindow):
    w, h = 0,0
    s_w, s_h = 0,0

    def get_old_height(self):
            return self.h
    def get_old_width(self):
            return self.w

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background: "+color_system.value[2]+";")

        if configuration == Configuration.CENTER_BAR:
            screen = QApplication.primaryScreen().availableGeometry()
            self.w, self.h = 600, 70
            self.setGeometry((screen.width() - self.w) // 2, ((screen.height() - self.h) // 2)-70, self.w, self.h)

        if configuration == Configuration.BOTTOM_RIGHT_BAR:
            screen = QApplication.primaryScreen().availableGeometry()
            self.w, self.h = 400, 150
            self.setGeometry(screen.width() - self.w - 10, screen.height() - self.h - 10, self.w, self.h)

        self.s_w, self.s_h = screen.width(), screen.height()
        shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        shortcut.activated.connect(open_settings)

    def reset_height(self):
        if configuration == Configuration.CENTER_BAR:
            self.setGeometry((self.s_w - self.w) // 2, ((self.s_h - self.h) // 2)-70, self.w, self.h)
        if configuration == Configuration.BOTTOM_RIGHT_BAR:
            self.setGeometry(self.s_w - self.w - 10, self.s_h - self.h - 10, self.w, self.h)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        if event.key() == Qt.Key_Q and event.modifiers() & Qt.ControlModifier:
            self.close()
        if event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            open_settings()

class NoteLineEdit(QPlainTextEdit):

    current_state = States.EDIT_RUNNING

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Tell Punch what's on your mind...")
        self.setStyleSheet("font-size: 16px; padding: 10px; color:"+color_system.value[0]+"; background:"+color_system.value[1]+"; border: none; outline: none;")
        self.setGeometry(10, 10, self.parent().width()-20, self.parent().height()-20)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_files")
        os.makedirs(notes_dir, exist_ok=True)
        self._notes_path = os.path.join(notes_dir, "note.txt")
        with open(self._notes_path, "a", encoding="utf-8"):
            pass

    def ask_notex(self, prompt):
        response = ask_mistral(prompt)
        self.setPlainText(response)
        self._adjust_height()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not (event.modifiers() & Qt.ShiftModifier):
                text = self.toPlainText().strip()
                if text.lower().startswith("/notex "):
                    self.current_state = States.AI_RUNNING
                    prompt = text[len("/notex "):].strip()
                    self.setReadOnly(True)
                    self.setPlainText("⏳")
                    QTimer.singleShot(100, lambda: self.ask_notex(prompt))
                else:
                    self.reset_height()
                    if self.current_state == States.EDIT_RUNNING:
                        if text :
                            self.write_text()
                        self.clear()
                        self.setReadOnly(True)
                        self.setPlainText("✓")
                        QTimer.singleShot(500, lambda: self.setPlainText(""))
                        QTimer.singleShot(500, lambda: self.setReadOnly(False))
                    else :
                        self.setPlainText("")
                        self.setReadOnly(False)
            else:
                if self.current_state == States.EDIT_RUNNING:
                    self.insertPlainText("\n")
                    self._adjust_height()
        else:
            super().keyPressEvent(event)

    def write_text(self):
        with open(self._notes_path, "a", encoding="utf-8") as file:
            file.write(datetime.now().strftime("%d/%m/%Y %H:%M"))
            file.write("\n")
            file.write(self.toPlainText())
            file.write("\n\n")

    def _adjust_height(self):
        fm = self.fontMetrics()
        line_h = fm.lineSpacing()
        lines = self.document().blockCount()
        padding = 20  # correspond au padding: 10px du stylesheet
        new_h = min(line_h * lines + padding + 10, MAX_HEIGHT)

        self.setFixedHeight(new_h)
        self.setGeometry(10, 10, self.parent().width() - 20, new_h)
        self.parent().setFixedHeight(new_h + 20)

    def reset_height(self):
        self.parent().setMinimumHeight(0)
        self.parent().setMaximumHeight(16777215)
        self.parent().reset_height()

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)

        old_w = self.parent().get_old_width()
        old_h = self.parent().get_old_height()
        self.setGeometry(10, 10, old_w - 20, old_h - 20)

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
