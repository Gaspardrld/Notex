from app import *
from hotkey import HotkeyListener
from PySide6.QtCore import QTimer
import ctypes
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


def toggle_window():
    if window.isVisible():
        window.hide()
    else:
        window.show()
        force_foreground(int(window.winId()))
        note_input.setFocus()



menu = QMenu()

open_action = QAction("Open")
open_action.triggered.connect(toggle_window)
menu.addAction(open_action)


setting_action = QAction("Settings")
setting_action.triggered.connect(open_settings)
menu.addAction(setting_action)

quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)


tray.setContextMenu(menu)
tray.activated.connect(lambda reason: toggle_window() if reason == QSystemTrayIcon.Trigger else None)

def force_foreground(hwnd):
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    
    fg_window = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_window, None)
    current_thread = kernel32.GetCurrentThreadId()
    
    user32.AttachThreadInput(fg_thread, current_thread, True)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(fg_thread, current_thread, False)

        

if __name__ == '__main__':
    listener = HotkeyListener()
    listener.triggered.connect(toggle_window)
    listener.start()
    window.hide()
    app.exec()