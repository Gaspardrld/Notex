import ctypes
import ctypes.wintypes
from PySide6.QtCore import QObject, Signal, QThread

MOD_CONTROL = 0x0002
WM_HOTKEY = 0x0312
HOTKEY_ID = 1

class HotkeyListener(QObject):
    triggered = Signal()

    def start(self):
        self._thread = _HotkeyThread(self)
        self._thread.triggered.connect(self.triggered)
        self._thread.start()

class _HotkeyThread(QThread):
    triggered = Signal()

    def run(self):
        ctypes.windll.user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL, ord(' '))
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                self.triggered.emit()
        ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID)
