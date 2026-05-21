from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPlainTextEdit, QSystemTrayIcon, QMenu, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction, QTextCursor
import os
import sys
from datetime import datetime

from user_files.user_config import*
from views.settings import SettingsWindow
from views.notifications import NotifWindow
from PySide6.QtGui import QShortcut, QKeySequence
from enum import*
from mistral_.mistral_retriever import ask_mistral
from assets.animation.shimmer_text_edit import ShimmerPlainTextEdit


MAX_HEIGHT = 400
class States(Enum):
    EDIT_RUNNING = 1 
    AI_RUNNING = 2
    AI_RUNNING_FINISH = 3
cond_ia = "/"

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
        shortcut.activated.connect(settings_window.open_settings)

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

class NoteLineEdit(ShimmerPlainTextEdit):

    current_state = States.EDIT_RUNNING

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("/ to ask Notex, or just write...")
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
        self.textChanged.connect(self.detect_changes)

    def detect_changes(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.detect_notex()
        if configuration == Configuration.CENTER_BAR :
            self._adjust_height()

    def detect_notex(self):
        text = self.toPlainText()
        if text.lower().startswith(cond_ia):
            self.current_state = States.AI_RUNNING
            self.setStyleSheet("font-size: 16px; padding: 10px; color: navy; background:white; border: none; outline: none;")
            self.parent().setStyleSheet("background: white;")
            self.start_shimmer()
        else :
            self.setStyleSheet("font-size: 16px; padding: 10px; color:"+color_system.value[0]+"; background:"+color_system.value[1]+"; border: none; outline: none;")
            self.parent().setStyleSheet("background: "+color_system.value[2]+";")
            self.current_state = States.EDIT_RUNNING
            self.stop_shimmer()

    def ask_notex(self, prompt):
        try :
            response = ask_mistral(prompt)
            self.setPlainText(response)
        except Exception as e: 
            self.setPlainText(f"Erreur : {str(e)[:100]}")
        self.current_state = States.AI_RUNNING_FINISH

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not (event.modifiers() & Qt.ShiftModifier):
                text = self.toPlainText().strip()
                if self.current_state == States.AI_RUNNING :
                    prompt = text[len(cond_ia):].strip()
                    self.setReadOnly(True)
                    self.ask_notex(prompt)
                    self_current_states = States.AI_RUNNING_FINISH
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
                        self.current_state = States.EDIT_RUNNING
            else:
                self.insertPlainText("\n")
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
notif = NotifWindow()


icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "icon.png")
icon = QIcon(icon_path)
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

app.setQuitOnLastWindowClosed(False)
window = MainWindow()


note_input = NoteLineEdit(window)
