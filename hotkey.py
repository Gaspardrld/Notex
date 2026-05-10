from PySide6.QtCore import QObject, Signal
from pynput import keyboard

class HotkeyListener(QObject):
    triggered = Signal()

    def start(self):
        def on_activate():
            self.triggered.emit()
        
        self.listener = keyboard.GlobalHotKeys({'<ctrl>+<space>': on_activate})
        self.listener.start()